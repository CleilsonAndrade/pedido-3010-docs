# Fluxo — Gravação do 1º pedido do master na 3010

Endpoint:

```text
POST /api/v1/gravacao      multipart: "arquivo" (o MESMO LAST da prévia) + "pedido" (JSON)
```

**Escreve no WinThor.** Só com `GRAVACAO_3010_ATIVA=S`. Escopo atual: **1º
pedido do master, sem frete**, com os impostos do cadastro. Validado na
homologação (`03_VALIDACOES/VALIDACAO_PRIMEIRO_PEDIDO_GRAVADO.md`); **não
publicado em produção**. A `QTSUGESTAO` foi homologada e implementada em
30/09/2026 para o caminho em que a filial não considera estoque pendente.

## 1. O servidor não confia na tela

```text
chave GRAVACAO_3010_ATIVA desligada           -> 403, sem ler nada
SHA-256 do arquivo ≠ o que a prévia devolveu  -> 409 ("não é o mesmo arquivo")
refaz a prévia do mesmo arquivo
cada pendência do LAST precisa de escolha válida (linha trocada ou ambíguo,
  com as mesmas opções da tela)
confere no WinThor: filial na PCLIB do usuário, fornecedor de importação não
  bloqueado, comprador, moeda, via, país, porto de chegada e de nacionalização
lê a COTAÇÃO (moeda + data) e a TRIBUTAÇÃO de cada produto no servidor
  (a tela não manda valor)
regra A na negociação; decisão D (motivo obrigatório se o fornecedor já tem
  master desta invoice)
qualquer problema                              -> 422 com a LISTA de problemas
```

## 2. O que a gravação deduz (sem campo na tela)

Evidência: roteiro 2.23 sobre 1.389 pedidos da 3010 em 2026
(`03_VALIDACOES/VALIDACAO_TEMPLATE_X_TRACE.md`).

```text
FRETE, TIPOVENC, TIPOEMBALAGEMPEDIDO, PERCAPRAZO   'C', 'P', 'V', 100 (767 de 775 primeiros pedidos)
CODFORNECFABRIC, CODFORNECPROD                     = CODFORNEC (1.389 de 1.389)
CODPAISPROC, CODPAISAQUISICAO                      = país de origem (1.389 de 1.389)
NUMPROFORMA                                        = invoice por padrão, editável na tela
DTEMISSAOINVOCE                                    data da invoice do LAST
DTPREVEMBARQUE                                     = data da invoice, editável
DTPREVCHEGADA                                      digitada na tela (27 a 41 dias, varia)
DTPREVENTRADAESTOQUE                               = chegada + 20 dias, editável
OBS a OBS6                                         vazias na criação
OBS7                                               "Invoice repetida: <motivo>", 100 caracteres
                                                   (OBS4, OBS6 e OBS7 nunca usadas em 2026)
```

Invoice e proforma vão **sem espaço em branco nas pontas** (há NUMINVOCE com
tabulação na base).

## 3. Itens

```text
mesmo produto em mais de uma linha   uma linha só: quantidade somada; preços diferentes
                                     pela média ponderada (total ÷ quantidade, 6 casas)
PESOLIQDI                            N.W. da linha ÷ quantidade (6 casas); o cadastro
                                     (PESOLIQDI, ou PESOLIQ) só quando o LAST não traz
tributação                           da consulta de impostos rodada NA gravação; item que
                                     ela não libera (podeUsar false) -> 422
CUSTOULTENT                          PCEST.CUSTOULTENT da filial na hora (NVL 0)
valores                              02_FLUXOS/CALCULO_DO_PEDIDO.md, sem frete
QTSUGESTAO                           QTGIRODIA × (PRAZOENTREGA + TEMREPOS) − ESTOQUE_DISPONIVEL
                                     negativo é preservado; pedido nativo 11866 reproduziu 2/2
```

## 4. A montagem

`api/src/modules/gravacao/`: as 136 colunas do PCPEDIDO e as 173 de cada
PCITEM **na ordem da 3010**, com os fixos gerados do template
(`colunas-3010.ts`), a montagem pura (`montagem.ts`) e o INSERT com valores
ligados por posição (`valor-sql.ts`: data como texto em `TO_DATE`, nunca `Date`;
NULL e SYSDATE no próprio SQL). Contrato das colunas em
`04_CONTRATOS/COLUNAS_PCPEDIDO_PCITEM.md`.

## 5. A execução (uma transação só)

```text
SELECT PROXNUMPED FROM PCCONSUM FOR UPDATE WAIT 5         -> NUMPED
UPDATE PCCONSUM  (+1)
SELECT PROXNUMPEDIDO FROM PCNUMERADORIMP ... FOR UPDATE WAIT 5
UPDATE PCNUMERADORIMP (+1)                                -> master "número/FFAA" (1049/0426)
confere: NUMPED já em PCPEDIDO ou PCITEM? master já em PCPEDIDO?  -> recusa, desfaz tudo
INSERT PCFORNECFILIAL (todos os fornecedores nas filiais que faltam, fora a 99)
INSERT PCITEM (cada item)  ->  INSERT PCPEDIDO
os três blocos PL/SQL da 3010, copiados do trace sem mudar uma letra:
  PCFORNEC (TIPOEMBALAGEMPEDIDO) · PCPRODUT (CUSTOREP, PESOLIQDI...) · PCPRODFILIAL
COMMIT        (qualquer falha no caminho: ROLLBACK de tudo, inclusive dos numeradores)
```

**Dois desvios intencionais em relação à 3010** (decisão de projeto):

1. **Uma transação só.** A 3010 confirma em pedaços (numeradores e
   PCFORNECFILIAL com COMMIT na hora): se algo falha, queima número e deixa
   fornecedor cadastrado pela metade. A aplicação não.
2. **Não apaga pelo NUMPED antes de gravar.** A 3010 faz `DELETE FROM PCPEDIDO
   WHERE NUMPED = :NUMPED` antes do INSERT; com o numerador atrasado (como o da
   homologação estava) isso apagaria um pedido de verdade. A aplicação confere e
   **para**.

A trava tem espera limitada: se outra sessão segura o numerador por mais de 5
segundos (ORA-30006, ou ORA-00054), a gravação recusa com 409 dizendo qual
numerador está ocupado e que dá para tentar de novo. Visto de verdade em 25/09.

O bloco do PCPRODUT faz `PCPRODUT.PESOLIQDI = PCITEM.PESOLIQDI`: gravar o peso do
LAST **corrige o cadastro** junto, como quando alguém digita o peso na 3010.

## 6. Respostas

```text
201   { numped, idPedidoMaster, invoice }
400   arquivo ou JSON faltando; campo em formato errado (ex.: data não AAAA-MM-DD)
403   gravação desligada
409   arquivo diferente do conferido; NUMPED ou master já existentes;
      numerador ocupado por outra sessão
422   { message, problemas: [...] }  o que impede gravar
```

## 7. Log da aplicação

Cada gravação registra NUMPED, master, invoice, fornecedor, quantidade de itens,
quem gravou e o **motivo completo** da invoice repetida (a OBS7 guarda só 100
caracteres).

## 8. Limites (ainda não validado)

```text
QTSUGESTAO        homologada para filial sem estoque pendente; se
                  CONSIDERAESTPENDSUGCOMPRA='S', a API recusa até esse ramo ser homologado
frete e despesas  calculados (02_FLUXOS/CALCULO_DO_PEDIDO.md), ainda não gravados
2º pedido         criado pela própria 3010; não se sabe qual ação o gera
produção          nenhuma gravação feita; a chave fica N até decisão
desfazer          previsto (só sem entrada, QTENTREGUE = 0), não implementado
```
