# Documentação — pedido-3010 (pedido master de importação na rotina 3010)

**Projeto:** `pedido-3010`
**Branch acompanhada:** `master`
**Data de referência:** 2026-09-28
**HEAD acompanhado:** `d3a0f53 feat: roteiro da QTSUGESTAO por NUMPED` (patch 0055 preparado)
**HEAD remoto acompanhado:** `origin/master` em `20fe04e` (0055 ainda não aplicado/publicado)
**Situação do checkpoint:** gravação do 1º pedido validada na homologação (base TESTE); produção bloqueada até a QTSUGESTAO ser conferida
**Serviços consumidos:** `comex-api` (leitura dos LASTs) · Oracle 19c do WinThor

---

<!-- DOC_VALIDACAO_TIME_2026_09_25:start -->

### Checkpoint atual — primeiro pedido gravado e validação do time da importação

Em 2026-09-25 a aplicação gravou o primeiro pedido na homologação:

```text
NUMPED           11858
IDPEDIDOMASTER   1049/0426
invoice          26MZC900F (LAST real com a invoice trocada)
itens            3
VLTOTAL          84.059,54
```

Conferido no banco (valores até a 6ª casa, numeradores, CUSTOREP do PCPRODUT
atualizado pelos blocos da 3010) e aberto na própria 3010 sem erro.

No mesmo dia o time da importação gravou 3 LASTs da semana e apontou: peso
líquido diferente do LAST, item repetido gravado duas vezes, e quatro avisos do
comex que não usa. As correções entraram em:

```text
0048 feat   prévia avisa o que não bloqueia
0049 fix    gravação soma o item repetido e grava o peso líquido do LAST
0050 feat   tela mostra os avisos
0051 fix    aviso do total FOB quando falta a soma do LAST
0052 feat   prévia dispensa os avisos do comex que o time não usa
0053 feat   aviso quando o peso do LAST difere mais de 10% do cadastro
```

O reteste com o código corrigido está pendente. Essa validação **não equivale a
publicação em produção**: a API rodava na máquina de teste, com a gravação ligada
só no `.env` local.
<!-- DOC_VALIDACAO_TIME_2026_09_25:end -->

## 1. Objetivo

Ler os LASTs da fábrica e gravar o **pedido master de importação na rotina 3010**
do WinThor, no lugar do lançamento à mão, com prévia e travas antes de gravar.

```text
usuário do setor 18 (IMPORTACAO), com usuário e senha do WinThor
   |
   v
tela (Angular)  ->  solta os LASTs
   |
   v
pedido-3010 API
   |
   |-- comex-api: lê a planilha e arredonda o preço como na invoice
   |-- de-para código de fábrica -> CODPROD
   |-- regras: código × descrição, negociação, invoice repetida, item repetido, peso
   |-- PRÉVIA: pendências (bloqueiam) e avisos (não bloqueiam)
   |
   |   o usuário escolhe filial, fornecedor, comprador, cotação, negociação, datas
   v
gravação na 3010 numa transação só (chave GRAVACAO_3010_ATIVA)
   |
   v
WinThor: PCPEDIDO + PCITEM + os blocos que a 3010 roda depois de gravar
```

A aplicação **não substitui a 3010**: grava o 1º pedido do master exatamente como
a 3010 grava; o 2º pedido continua sendo criado pela própria 3010.

## 2. Estado validado

- a prévia lê os LASTs pelo comex, resolve o de-para e aplica as regras; nenhuma
  rota além da gravação escreve no banco (há teste);
- o cálculo do 1º pedido reproduz a homologação: 71 de 71 itens, VLTOTAL a até 2
  centavos;
- a gravação monta as 309 colunas como a 3010 (teste de ouro contra o template e
  o trace) e grava numa transação só, conferindo tudo de novo no servidor;
- a tela coleta o que o pedido precisa e grava com confirmação;
- a gravação foi validada na homologação (11858); **não foi publicada em
  produção**.

### Gate (25/09)

```text
API unidade        318 / 318 PASS
API ponta a ponta  48 PASS, 2 pulados
tela               69 / 69 PASS
tsc / eslint / build        PASS
regra do teste de regressão PASS
```

## 3. Evidência de referência

O pedido 11681, lançado pela própria 3010 com trace, é a referência de tudo o que
a gravação reproduz (sequência, colunas, blocos PL/SQL):
`03_VALIDACOES/EVIDENCIAS_TRACE_E_BANCO.md`.

## 4. Onde começar

Leia nesta ordem:

1. `00_STATUS/STATUS_PEDIDO_3010.md`
2. `01_ARQUITETURA/VISAO_GERAL.md`
3. `01_ARQUITETURA/FRONTEIRA_COMEX_API_WINTHOR.md`
4. `01_ARQUITETURA/AUTENTICACAO_WINTHOR.md`
5. `01_ARQUITETURA/DECISOES.md`
6. `02_FLUXOS/PREVIA_DOS_LASTS.md`
7. `02_FLUXOS/CALCULO_DO_PEDIDO.md`
8. `02_FLUXOS/GRAVACAO_NA_3010.md`
9. `02_FLUXOS/TELA_DE_CONFERENCIA.md`
10. `03_VALIDACOES/EVIDENCIAS_TRACE_E_BANCO.md`
11. `03_VALIDACOES/ROTEIRO_QTSUGESTAO.md`
12. `03_VALIDACOES/VALIDACAO_HOMOLOGACAO_RODADAS.md`
13. `03_VALIDACOES/VALIDACAO_TEMPLATE_X_TRACE.md`
14. `03_VALIDACOES/VALIDACAO_PRIMEIRO_PEDIDO_GRAVADO.md`
15. `03_VALIDACOES/VALIDACAO_TIME_IMPORTACAO_3_LASTS.md`
16. `04_CONTRATOS/CONTRATO_COMEX_API.md`
17. `04_CONTRATOS/CONTRATO_API_PEDIDO_3010.md`
18. `04_CONTRATOS/COLUNAS_PCPEDIDO_PCITEM.md`
19. `05_OPERACAO/CONFIGURACAO_E_EXECUCAO.md`
20. `05_OPERACAO/ROTEIRO_HOMOLOGACAO.md`
21. `05_OPERACAO/BASE_TESTE.md`
22. `05_OPERACAO/SERVIDOR_E_PUBLICACAO.md`

`CHANGELOG.md` registra a evolução documental.

## 5. Regra documental

A documentação distingue comportamento **observado em runtime** (homologação),
**contrato coberto por teste**, **decisão** e **limite ainda não validado**.
Cada documento diz sua natureza no começo.

Não transformar evidência de um pedido ou de um LAST específico em regra universal
do WinThor ou da 3010. Quando for hipótese, dizer que é hipótese, e registrar
quando ela cair.

Não registrar senha, `.env` real, preço de fornecedor nem LAST neste repositório.

`DOCUMENTACAO_ATIVA_COMPLETA.txt` é derivado dos documentos canônicos e deve ser
regenerado com `tools/regenerate_consolidated.py`.

## 6. De onde veio cada documento

Até 2026-09-25 a documentação ficava na pasta `docs/` do repositório do código:

```text
docs/CONTINUAR.md    §0-§2   -> 00_STATUS/STATUS_PEDIDO_3010.md, 01_ARQUITETURA/VISAO_GERAL.md
                     §3      -> 03_VALIDACOES/VALIDACAO_HOMOLOGACAO_RODADAS.md
                     §4      -> 01_ARQUITETURA/DECISOES.md
                     §5      -> 03_VALIDACOES/EVIDENCIAS_TRACE_E_BANCO.md
                     §6-§9   -> 00_STATUS/STATUS_PEDIDO_3010.md, 05_OPERACAO/CONFIGURACAO_E_EXECUCAO.md
docs/GRAVACAO.md             -> 02_FLUXOS/GRAVACAO_NA_3010.md, 03_VALIDACOES/*,
                                04_CONTRATOS/COLUNAS_PCPEDIDO_PCITEM.md, 05_OPERACAO/BASE_TESTE.md
docs/HOMOLOGACAO.md          -> 05_OPERACAO/ROTEIRO_HOMOLOGACAO.md
docs/SERVIDOR.md             -> 05_OPERACAO/SERVIDOR_E_PUBLICACAO.md
```

O `CONTINUAR.md` deixou de existir: o `00_STATUS` faz o papel dele, inclusive o de
retomar o projeto num chat novo.
