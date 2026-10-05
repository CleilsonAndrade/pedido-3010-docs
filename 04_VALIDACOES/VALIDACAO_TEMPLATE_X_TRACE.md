# Validação — Template × trace da 3010 e o teste de ouro da montagem

**Natureza:** evidência + contrato coberto por teste.

## 1. As duas fontes

```text
trace do pedido 11681   o que a 3010 gravou de verdade; corta em 100 valores por comando
template P1             Template_-_PEDIDO_MASTER_3010.xlsx, aba INSERTS: as 136 + 173
                        colunas completas para o mesmo pedido de exemplo
                        (9018, 1.000 un a 83,74 USD, cotação 5,30, sem frete)
```

O template fica **fora do Git** (é planilha de trabalho do time). O que importa
dele está em `05_CONTRATOS/COLUNAS_PCPEDIDO_PCITEM.md` e nas fixtures do
repositório do código (`api/test/fixtures/template-3010-p1.json` e
`trace-11681-inserts.json`).

## 2. O cruzamento (24/09)

O template gera o pedido de exemplo P1 (9018, 1.000 un, 83,74 USD, 5,30), o
mesmo do trace. Coluna a coluna, onde os dois têm valor:

| Tabela | Colunas | Iguais | Diferentes | Só no template (depois do corte do trace) |
|---|---|---|---|---|
| PCITEM | 173 | 97 | 3 | 73 |
| PCPEDIDO | 136 | 96 | 4 | 36 |

As diferenças são todas explicadas: variáveis do pedido (NUMPED, master,
invoice de teste), a mesma data escrita de outro jeito (DATALANC = SYSDATE), e
duas escolhas do template: **CUSTOULTENT** lido do PCEST (a regra fechada na
3ª rodada) e **QTSUGESTAO = 0**, onde a 3010 gravou −2.316. Essa diferença de
`QTSUGESTAO` é histórica do template: em 30/09/2026 a conta foi homologada com
o pedido nativo 11866 e passou a ser calculada pela aplicação; ver
`04_VALIDACOES/ROTEIRO_QTSUGESTAO.md`. As colunas "só template" não têm como ser
conferidas pelo trace; quase todas são 0, NULL ou marcações ('S'/'N').

## 3. O teste de ouro da montagem (coberto por teste)

```text
entradas do pedido de exemplo  -> a montagem reproduz as 309 colunas do template
entradas do 11681              -> a montagem reproduz os 200 valores do trace
                                  (fora o DATALANC, que vai como SYSDATE)
```

Duas sabotagens de propósito foram pegas pelo teste, com a mensagem apontando a
coluna:

```text
FRETE 'C' trocado por 'F'      -> "FRETE: esperado 'C', montado F"
VLIPI com a conta do PIS        -> "VLIPI: esperado 34.618116, montado 9.320262"
```

## 4. Cabeçalho do 1º pedido: o que a 3010 grava (roteiro 2.23, 25/09)

Sobre 1.389 pedidos da 3010 em 2026 (775 são 1º pedido do master):

| Coluna | Regra na gravação | Evidência |
|---|---|---|
| FRETE, TIPOVENC, TIPOEMBALAGEMPEDIDO, PERCAPRAZO | **fixos 'C', 'P', 'V', 100** | 767 de 775 primeiros pedidos (o vazio/'S' é do 2º pedido) |
| CODFORNECFABRIC, CODFORNECPROD | = CODFORNEC | 1.389 de 1.389 |
| CODPAISPROC, CODPAISAQUISICAO | = país de origem | 1.389 de 1.389 |
| NUMPROFORMA | = invoice por padrão, **editável na tela** | 1.300 de 1.389; quando difere, costuma ser proforma de verdade (26MCS415F × 26MCS400F) |
| DTEMISSAOINVOCE | data da invoice do LAST | template (LEIA-ME) |
| DTPREVEMBARQUE | = data da invoice, editável | quase sempre 0 dias (às vezes 2 a 4) |
| DTPREVCHEGADA | **campo novo na tela** | 27 a 41 dias depois do embarque, varia |
| DTPREVENTRADAESTOQUE | = chegada + 20 dias, editável | a combinação mais comum em todas as faixas |
| OBS a OBS7 | vazias na criação, fora o motivo da decisão D | ver abaixo |

**OBS:** o time anota nelas ao longo da vida do pedido (OBS: "PEDIDO EM
PRODUÇÃO", "DUIMP ... INVOICE ... CNTR ..."; OBS3: "ITENS A ENDEREÇAR"; OBS5:
"PAGAMENTO SALDO EFETUADO"; OBS2 só no 2º pedido). **OBS4, OBS6 e OBS7 não
aparecem em nenhum pedido de 2026.** Cada uma tem 100 caracteres. **Decidido
(Cleilson, 25/09): o motivo vai na OBS7** ("Invoice repetida: ...", até 100
caracteres), com o texto completo no log da aplicação.

**Achado de dados:** há NUMINVOCE e NUMPROFORMA gravados com tabulação no fim
('26PGBK054\t', '26MDH530F\t\t'). A checagem de invoice repetida usava o TRIM
do Oracle, que só tira espaço, e essas invoices escapavam; corrigido (patch
0040). A gravação grava a invoice sem espaço em branco nas pontas.
