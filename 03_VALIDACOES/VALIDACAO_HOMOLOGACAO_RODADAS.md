# Validação — Rodadas de homologação (MIMO-HOMOLOG, base TESTE)

**Natureza:** registro histórico. Cada rodada é o que se observou **naquele
dia**, com o código daquele dia; não descreve o estado atual (ver
`00_STATUS/STATUS_PEDIDO_3010.md`). Migrado do §3 do antigo `CONTINUAR.md`,
com os ponteiros trocados para os documentos deste repositório.

**Como ler:** "Confirmado" é comportamento observado no banco da homologação;
"CORRIGIDO" é defeito nosso que virou teste de regressão; "Hipótese" é o que
ainda não tinha evidência, e o texto diz quando uma hipótese caiu.

| Rodada | Data | O que fechou |
|---|---|---|
| 1ª a 3ª | 23/09 | Consultas contra o banco real; IDPEDIDOMASTER é texto; CUSTOULTENT do PCEST no 1º pedido; frete rateado por PESOLIQDI × QT |
| 4ª a 7ª | 24/09 | O frete e as despesas do 1º pedido (a hipótese "frete só no 2º pedido" caiu na 6ª) |
| 8ª a 12ª | 24/09 | **Cálculo do 1º pedido fechado**: 71 de 71 itens iguais; VLTOTAL a até 2 centavos |
| 17ª | 24/09 | **Backend inteiro contra a homologação**: login, cadastros, cotação, impostos, prévia com LAST real |
| 25/09 | 25/09 | Item 2.23 (cabeçalho do 1º pedido); numerador de master acertado; primeiro pedido gravado (ver `VALIDACAO_PRIMEIRO_PEDIDO_GRAVADO.md`) |

---

## Pronto e testado

- **Etapa 1** (prévia, sem gravar nada): login, `POST /previa`, cadastros,
  sugestão de negociação, saúde, Swagger com o fluxo.
- **Testes:** 318 de unidade e 50 ponta a ponta (API); 69 da tela (2 deles só rodam com o
  comex-api no ar e a pasta de planilhas). **Todos rodam no fuso de
  Brasília** (`test/apoio/fuso-brasilia.js`, globalSetup das duas
  configurações do Jest), para erro de fuso não passar calado. Um teste
  falha se alguma rota ficar sem documentação no Swagger, e outro se alguma
  rota escrever no banco.
- **comex-api com a rota `/leitura`:** 271 testes passando (266 antigos + 5 novos).
- **Scripts:** regra de regressão 7/7, backup 19/19, shellcheck sem avisos.
- **Ensaio com 33 planilhas reais** (13 de set/2026 + 20 LASTs antigos),
  198 itens: 22 pedidos prontos para gravar, 11 travados (código trocado ou
  sem de-para, porque o de-para do ensaio veio da planilha do time, parada em
  06/08).

- **Roteiro de homologação** (`npm run homologacao`, `05_OPERACAO/ROTEIRO_HOMOLOGACAO.md`):
  roda as consultas da APLICAÇÃO contra a base numa transação somente
  leitura (e recusa o que não for SELECT/WITH) e gera um relatório `.md`
  com ok / diferente / erro por item. Ensaiado contra banco falso (21
  testes) e o comando real com driver falso: para em base que não é a
  172.20.20.13, abre READ ONLY, só consulta, ROLLBACK no fim, relatório
  sem senha.

## Homologação, 1ª rodada (23/09): só o banco, com a API desligada

Serviço **TESTE** em mimo-homolog, 172.20.20.13 (a documentação antiga dizia CDBTST).
Resultado: 14 ok · 3 diferente · 2 erro (API desligada) · 6 info · 4 pulado.
A base é uma cópia recente da produção (pedidos até o 11849, de ~22/09).

**Confirmado:**
- região padrão da filial 4 = 300 (a hipótese do `:NUMREGIAO` da tela);
- datas da cotação sem hora; a aplicação trouxe a cotação do dia pedido, e a
  de 19/07/2026 = 5,30, a do trace;
- país de origem = procedência = aquisição em todos os pedidos de 2026;
- 11840/11841: invoice 26MCS415F, fornecedor 15 (HANGZHOU CHOICE TRADE CO.,
  LTD), negociação 26580, masters **diferentes** (1046/0426 e 1047/0426), o
  11841 com proforma 26MCS400F. Os testes usam agora esses valores reais;
- impostos do 9018 = 20 / 6,5 / 2,1 / 9,65, como no trace;
- 105 de 121 itens dos últimos 20 pedidos com os mesmos percentuais que a
  tela gravou;
- de-para: 1.883 de 1.931 iguais à planilha do time, em 2,2 s. Invoice
  repetida em 18 ms: o `UPPER(TRIM())` sem índice não pesa;
- parâmetros da tela nesta base: TIPOTRIBENTIMP = F, CON_USATRIBUTACAOPORUF = N;
- a sugestão de negociação daria 26625 (maior de 26: 26624).

**Erro nosso, CORRIGIDO:** o IDPEDIDOMASTER é **texto** (`1046/0426`). A
consulta de invoice repetida convertia para número e devolvia `null`
(teste de regressão em `pedidos-da-invoice.oracle.spec.ts`). Para a etapa 3:
o master é gerado como texto. Hipótese do formato: sequência / filial com 2
dígitos + ano com 2 dígitos. O item 1.11 do roteiro mostra por filial.

**Em aberto na 1ª rodada** (o que a 2ª respondeu está na seção seguinte):
- **PERCDESCICMSDIF trava o item.** A figura do 9018 tem 100 e o PCITEM do
  trace tem 0, então o item sai `podeUsar` false, até o próprio caso do trace.
  Hipótese: a tela não copia esse campo, que só pesa quando há ICMS (e
  PERICM = 0). O item **2.15** compara campo a campo consulta × PCITEM.
  Só mexer na lista com essa evidência, e com teste.
- **II 14,4 gravado × 25 no cadastro** em todos os itens dos pedidos 11823 e
  11849. Hipóteses: o cadastro mudou depois; alguém alterou na tela
  (decisão 3); ou há um campo que reduz o II e não está na consulta. O item
  **2.14** traz a emissão, quem lançou e o histórico de cada produto.
- **Porto:** 1 pedido de 2026 (9726) com chegada 1 ≠ nacionalização 3. O
  item **2.16** calcula com os dois e diz qual reproduz o PCITEM.
- **De-para, 48 diferenças.** Parecem erro de digitação da planilha do time
  (10874 × 10784, 1004 × 10004, 8797 × 8297) e CODFAB duplicado no WinThor
  (família HTC, que dá "ambíguo" e vira pendência a cada LAST). O item
  **2.11** traz as duas descrições e os candidatos.
- **CUSTOULTENT (item 1 dos pontos em aberto (00_STATUS)).** A tela gravou 7 valores diferentes para o
  9018 na filial 4 em 2026, alternando até no mesmo dia (31/07: 862,09 no
  11296 e 732,22 no 11342). Não é só o PCEST da filial. O item **1.12**
  procura cada valor nos custos do PCEST de todas as filiais.
- **Dado da base:** cotação da moeda 220 com data 30/03/2105 (3,1915).
  Digitação errada na homologação, e talvez na produção. O item 1.10 lista.

## Homologação, 2ª rodada (23/09): banco e API no ar, sem login

Resultado: 15 ok · 4 diferente · 0 erro · 10 info · 5 pulado. O grupo 3
parou no login, porque o roteiro rodou sem HOMOLOG_USUARIO/HOMOLOG_SENHA
naquele terminal. A API respondeu `/saude` com banco e comex no ar.

**Confirmado com evidência:**
- **Os campos da tributação são cópia do cadastro, com o mesmo nome** (2.15):
  36 campos batem em 96 de 96 itens recentes, entre eles PERIPI, PERPIS,
  PERCOFINS, CODSITTRIBPISCOFINS, PERCICMSDIFERIDO, CALCCREDIPI, PERICM,
  seguro e despesas.
- **CUSTOULTENT = PCEST.CUSTOULTENT da filial na hora do lançamento** (2.15):
  95 de 96 itens recentes batem com o PCEST de hoje. Os valores antigos do
  9018 não aparecem em nenhum custo atual (1.12), o que combina com o PCEST
  mudando a cada entrada. Resta explicar valores fora de ordem como o do
  11723. Hipótese: o 2º pedido do master copia o custo do 1º (item 1.14).
- **Formato do IDPEDIDOMASTER** (1.11): `número/FFAA`, com a filial em 2
  dígitos e o ano em 2 (`1041/0126` na filial 1, `1046/0426` na filial 4).
  O número é um só para todas as filiais no ano: 1041, 1046 e 1047 no mesmo
  dia, em filiais diferentes.
- **O trace confirma o numerador:** no pedido 11681, a tela fez SELECT e
  UPDATE no PCNUMERADORIMP do ano e gravou `942/0426`.

**Erros nossos, CORRIGIDOS (com teste de regressão):**
- **PERCDESCICMSDIF travava todo item.** O cadastro tem 100 e a tela grava 0
  em 96 de 96 itens: ela não copia. Saiu da lista de "fora do cálculo".
  Só age sobre ICMS, que o PERICM já guarda. Na gravação: 0, como a tela.
- **O porto da tributação é o de NACIONALIZAÇÃO** (2.16). No pedido 9726
  (chegada 1, nacionalização 3), os 6 itens batem com o porto 3 e nenhum com
  o porto 1. A rota pedia o de chegada. O parâmetro virou
  `portoNacionalizacao`, e o nome antigo dá 400.

**Para a gravação (etapa 3):** VLIPIPORKG e VLPAUTAIPI ficam vazios no
PCITEM, como a tela faz, e PERCDESCICMSDIF fica 0.

**Em aberto, com evidência nova. A 3ª rodada do roteiro traz o resto:**
- **FRETE: o cálculo não cobre, e 70% dos itens recentes têm frete.** Em 68
  de 96 itens a tela gravou PERCFRETE próprio (11,89 / 11,19 / 19,76 no
  11849). Não vem do cadastro, que tem 0. É o frete do pedido
  (PCPEDIDO.VLFRETE) repartido por item, e **não por valor**, porque o
  percentual muda de item para item. O cálculo só foi conferido com frete 0.
  O item **2.17** confere o cálculo item a item (sem frete: os 6 valores e o
  VLTOTAL; com frete: quatro formas de base). O item **2.18** testa o
  rateio contra cada coluna do PCPRODUT. **A tela e a gravação dependem disso.**
- **PCNUMERADORIMP da homologação está ATRÁS** dos masters: próximo 406,
  com masters em uso até 1047. Os masters 399 a 405 são os pedidos de teste
  do template. Gravar na homologação hoje geraria `406/0426`, que já existe.
  Na etapa 3, a gravação confere se o master existe e **para** (nunca
  "conserta" o numerador). Conferir na produção e perguntar por que a
  homologação está assim (item 1.13).
- **II 14,4 × 25 no 11849** (18/09, NICOLY.SOARES, 12 itens). O histórico
  dos outros produtos mostra II mudando no tempo (18 → 20 → 25, e até 0 no
  11490). O 2.14 passa a trazer o histórico destes produtos primeiro.
- **Pedidos 11851 a 11857** (ANDREIA.Y): número maior que o do 11849
  (18/09), mas emissão em 01/08, e os 9 itens estão "sem tributação" hoje.
  Hipótese: são 2º pedidos de master. O 2.14 passa a mostrar o
  NUMPEDMASTERORIGEM e o motivo completo.
- **De-para, 30 ambíguos, 27 da família HTC.** Cada código tem o produto
  original (`12415 HTC0080-Torn...`) e um duplicado recente com "MP" na
  descrição (`17639 MP HTC0080-...`, códigos 176xx a 178xx). A planilha do
  time sempre escolhe o original. O 2.11 passa a procurar a coluna do
  PCPRODUT que separa os dois (hipótese: IMPORTADO). As 13 diferenças de
  CODPROD parecem erro de digitação da planilha (10874 × 10784,
  1004 × 10004), e o banco está certo.

## Homologação, 3ª rodada (23/09): o frete resolvido

Resultado: 14 ok · 5 diferente · 3 erro · 12 info · 4 pulado. O grupo 3 não
rodou porque a API estava desligada ("fetch failed"). O item 2.11 deu erro no
próprio roteiro (LOB no `SELECT *` do PCPRODUT), já corrigido com teste.

**O cálculo reproduz a tela, agora com evidência larga:**
- **Sem frete: 37 de 37 itens** com base, II, PIS, COFINS, IPI e custo
  iguais aos gravados. Antes era só o 9018 do trace.
- **VLTOTAL: 4 de 4 pedidos sem frete feitos pela tela** batem. Os 7 "não"
  eram os 11851 a 11857, que têm **VLTOTAL vazio e porto de nacionalização
  vazio**. Não parecem lançados pela tela, e o roteiro agora os deixa de fora.

**A regra do frete, deduzida e conferida até a 6ª casa (pedido 11849, 14 itens):**
```
frete por unidade = frete total × PESOLIQDI ÷ Σ(PESOLIQDI × QT)          (sem arredondar)
  VLFRETE   = frete por unidade, 6 casas                        → 14 de 14
  PERCFRETE = frete por unidade ÷ PCOMPRA × 100, 6 casas        → 14 de 14
  base      = (PCOMPRA + frete por unidade) × COTACAO           → 68 de 68 na forma; 3 de 3 até a 6ª casa
  II, PIS, COFINS, IPI: a mesma conta, sobre essa base
```
- O rateio é pelo **PCPRODUT.PESOLIQDI × QT**, que explica 9 de 9 pedidos.
  Valor, quantidade, peso bruto e volume não explicam.
- **Na base entra o frete sem arredondar.** Com o VLFRETE arredondado, a base
  erra na 6ª casa. O rateio devolve os dois valores.
- O frete total está na moeda do pedido (7.100 USD no 11849). **O
  PCPEDIDO.VLFRETE veio vazio**, então a coluna onde a tela guarda o total
  ainda não se sabe. O item 2.19 procura no PCPEDIDO e no PCCONTAINERS.
- **Implementado:** `calculo/frete.calculo.ts` (`ratearFrete`) e o
  `freteUnitario` em `calcularValoresItem`, com os dados reais do 11849 como
  teste (`test/fixtures/homologacao-11849-frete.json`). A 4ª rodada confere
  os pedidos inteiros com frete, VLTOTAL incluído, pelo cálculo novo.

**Item 1 do pontos em aberto (00_STATUS) (CUSTOULTENT), FECHADO:** no 1º pedido do master, a tela grava o
PCEST.CUSTOULTENT da filial na hora (95 de 96 itens). O **2º pedido copia o
custo do 1º**: 24 de 24 no 9018 da filial 4 (1.14). O 11723 é 2º do 11254,
por isso tem 732,22. A aplicação só cria o 1º, então vale o PCEST.

**II 14,4 × 25 (11849 e 11629):** o 8814 teve 14,4 de 2024 a 2025, 25 em junho
de 2026 e 14,4 de novo em 18/09. O 10582 também voltou a 14,4 num pedido da
FLAVIA.SILVA em 26/08, com o cadastro em 25. Parece alteração manual na tela,
o que a decisão 3 permite. Perguntar a quem lançou por que 14,4.

**Numerador:** a homologação continua com próximo 406 e maior master em uso
1048 (1.13).

## Homologação, 4ª rodada (24/09): o que o frete ainda não explica

Resultado: 15 ok · 6 diferente · 1 erro · 12 info · 5 pulado. O login pulou
de novo (sem usuário/senha no processo), e o 2.19 caiu porque o PCCONTAINERS
não tem NUMPED. Os dois estão corrigidos com teste: o PCCONTAINERS liga pelo
**IDCONTROLEEMBARQUE** (trace, entrada 314), e o 3.2 diz qual variável faltou.

**Confirmado de novo:**
- sem frete: 28 de 28 itens e VLTOTAL 4 de 4;
- com frete: base, II, PIS, COFINS, IPI, VLFRETE e PERCFRETE batem pelo
  cálculo novo, com rateio pelo PESOLIQDI.

**Ainda NÃO bate com frete (a 5ª rodada procura a fórmula, item 2.20):**
- **CUSTOULTPEDCOMPRA ≠ base + II.** O gravado é menor, e falta perto de
  79,5% do frete em reais, mas não exato (0,7938 a 0,7977 no 11849). O custo
  usa outro valor, e o PCITEM tem colunas de custo que o cálculo nunca olhou:
  VLFRETENFCUSTO, VLAFRMMCUSTO, VLSISCOMEXCUSTO, VLADUANEIRACUSTO,
  VLCAPATAZIACUSTO, VLOUTROSCUSTOS...
- **VLTOTAL gravado > calculado** nos 9 pedidos com frete. A sobra dividida
  pelo frete em USD é **igual entre pedidos do mesmo processo** (11840/11841:
  1,2212; 11838/11839: 1,1627; 11831 a 11833: 1,1625) e diferente entre
  processos (11849: 0,4703). Cara de despesa do processo (capatazia, AFRMM,
  Siscomex...). É hipótese.
- Erro do roteiro, corrigido: o "38 de 68 iguais" contava pela lista limitada
  a 30 linhas. Provavelmente nenhum item com frete bate no custo.

**Enquanto isso não fechar:** pedido com frete pode ter os impostos e o VLFRETE
calculados pela aplicação, mas **não o VLTOTAL nem o custo**. A prévia tem que
mostrar isso como pendência, e a gravação não grava pedido com frete. A 5ª
rodada indica que isso nem acontece no 1º pedido (ver abaixo, item 2.21).

## Homologação, 5ª rodada (24/09): a API inteira, e o frete é do 2º pedido

Resultado: 19 ok · 6 diferente · 0 erro · 14 info · 1 pulado.

**API no ar, pelo caminho inteiro, OK:** login WinThor (setor 18) com token;
`/cadastros/filiais` com 32 filiais, entre elas a 4 (PCLIB do usuário);
`/cadastros/cotacao` de 15/09 = 5,1696, igual à consulta direta (DTO e
consulta, a correção do fuso); `/cadastros/impostos` do 9018 = 20 / 6,5 /
2,1 / 9,65. Falta só o `/previa` com um LAST de verdade (`PLANILHA=`).

**Frete: por que nenhuma fórmula explica o custo e o VLTOTAL** (2.20 sem
fórmula de 1 ou 2 colunas; 2.17 com a contagem corrigida: 0 de 68 no custo).
O pedido inteiro do 11849 mostra:
```
NUMPEDMASTERORIGEM = NUMPEDPRINC = 10874      → é o 2º PEDIDO do master; o 1º é o 10874
QTENTREGUE = QTPEDIDA · NUMTRANSENTN 736355   → já teve entrada
VLTOTAL 381.253,43 · VLENTREGUE 381.253,42    → o VLTOTAL é o valor da entrada
VLSISCOMEX, VLAFRMM = base × PERCSISCOMEX/PERCAFRMM (8 de 10 exatos)  → despesas da DI
II 14,4, e o 10874 gravou 25                  → o II da DI
```
**Hipótese (REFUTADA na 6ª rodada, ver abaixo):** pedido com frete = 2º pedido, que a própria 3010 cria na
nacionalização com os valores da DI e da nota de entrada. Custo e VLTOTAL
vêm da entrada, e não de uma fórmula sobre o pedido. **Se valer para todos, o
1º pedido (o único que a aplicação cria) não tem frete**, e o cálculo dele já
está provado (28 de 28 itens, VLTOTAL 4 de 4). O item **2.21** confere nos 13
pedidos. Nesse caso o `ratearFrete` fica no código, conferido, mas fora da
prévia e da gravação. Isso também explicaria o II 14,4 do 11849 e do 11629
(DI, não alteração manual). O 2.19 não achou o frete total no PCPEDIDO nem no
PCCONTAINERS (vazio para o 11849), e o PCITEM.PESOLIQDI é o do cadastro em 68
de 68.

## Homologação, 6ª rodada (24/09): o 1º pedido TEM frete

**A hipótese caiu (2.21):** só 2 dos 9 pedidos com frete são 2º pedido
(11849 do 10874, 11845 do 11677, os dois com entrada e VLTOTAL = VLENTREGUE).
Os outros 7 (11831 a 11833, 11838 a 11841) são **1º pedido, sem entrada,
com frete**. Os 4 sem frete são 1º pedido. **O frete importa para a
aplicação.**

Isso também explica o 2.20 sem fórmula: a busca misturava 1º e 2º pedidos, e
no 2º pedido custo e VLTOTAL vêm da nota de entrada.

**Nos 1º pedidos com frete (11840 e 11841, os que vieram no detalhe):** base,
II, PIS, COFINS, IPI, VLFRETE e PERCFRETE batem. Só não batem:
- **CUSTOULTPEDCOMPRA:** o gravado é menor que base + II. No 11840 faltam
  exatamente 70,069930 nos dois itens (9988 e 9989), então a diferença não
  depende do preço;
- **VLTOTAL:** o gravado é maior. A sobra dividida pelo frete em USD é igual
  entre pedidos do mesmo processo (11840/11841: 1,2212; 11838/11839: 1,1627;
  11831 a 11833: 1,1625).

**Roteiro corrigido (com teste):** o 2.20 busca só em 1º pedido, e tenta 3
colunas de valor quando 1 ou 2 não bastam. O exemplo detalhado passa a ser
um 1º pedido com frete. O 2.17 separa 1º e 2º pedido. O 3.6 avisa quando o
arquivo da `PLANILHA` não existe: na rodada foi usado o caminho de exemplo.

## Homologação, 7ª rodada (24/09): as despesas do 1º pedido, deduzidas do 11841

A busca do 2.20 ainda não achou fórmula, mas por um erro do roteiro:
colunas **nulas** em alguns itens (VLADUANEIRA sem despesa) sumiam da busca
inteira. Está corrigido com teste (`colunasNumericasEmAlguma`, nula vale 0).
Com o 1º pedido 11841 inteiro, a conta fechou à mão:

```
Todas as despesas do pedido são repartidas por PESOLIQDI × QT (mesmo valor por kg em todos os itens):
  frete (VLFRETE)                6.800 USD   → base, II, IPI, PIS, COFINS (já no cálculo)
  desp. aduaneira (VLADUANEIRA)  4.700 R$
  outros custos (VLOUTROSCUSTOS) 4.500 R$
  AFRMM (VLAFRMM)                3.604 R$  = exatamente 10% do frete em reais (36.040)

VLTOTAL = Σ QT × (base + II + IPI + PIS + COFINS + aduaneira + AFRMM)
          321.503,29 calculado × 321.503,27 gravado (centavos de arredondamento)

CUSTOULTPEDCOMPRA = PCOMPRA × COT + II + aduaneira + outros custos + AFRMM + X
          X = 3.196,00 R$ no pedido, também por peso, SEM coluna no PCITEM
          → RESOLVIDO na 8ª rodada: X + AFRMM = o frete em DÓLAR (ver abaixo)
```

**O que isso muda na tela (etapa 2):** o 1º pedido tem despesas do processo,
digitadas como **totais do pedido**: frete (USD), despesa aduaneira, outros
custos, AFRMM (ou 10% do frete?) e o X do custo. A aplicação reparte tudo
por PESOLIQDI × QT, com o mesmo `ratearFrete`. Ainda não se sabe **onde a
3010 guarda esses totais**: não estão no PCPEDIDO nem no PCCONTAINERS.

**O caminho mais curto:** um trace novo da 3010 (igual ao
TRACE3010_-_PEDIDO_MASTER_2.log) lançando **na homologação** um pedido com
frete e despesas. Ele mostra os campos da tela, a tabela dos totais, o X do
custo e o que a gravação escreve. O 2.20 da 8ª rodada, com a busca corrigida,
confere o padrão nos 7 pedidos (`despesasPorPedido`: totais, AFRMM ÷ frete e
X de cada um).

## Homologação, 8ª rodada (24/09): as regras do 1º pedido com despesas, FECHADAS

O resumo de despesas do 2.20 nos 7 primeiros pedidos com frete mostrou:
```
AFRMM ÷ frete em reais = 0,100 em todos                      → AFRMM = 10% do frete
X (a sobra do custo) + AFRMM = frete em USD em todos:
  11841: 3.196 + 3.604 = 6.800 · 11840: 6.392 + 7.208 = 13.600 · 11839: 10.475 + 11.812 = 22.287
```
**Regras deduzidas e conferidas até a 6ª casa no 11841** (fixture
`test/fixtures/homologacao-11841-despesas.json`):
```
Totais do pedido repartidos por PESOLIQDI × QT (por unidade, sem arredondar):
  frete (USD) · despesa aduaneira (R$) · outros custos (R$) · AFRMM (R$, total informado:
  10% do frete em reais SEM os centavos nos 7 pedidos — corrigido na 9ª rodada)
base              = (PCOMPRA + frete) × COT                        → II, PIS, COFINS, IPI como antes
PERCADUANEIRA, PERCAFRMM = despesa ÷ base × 100
PERCOUTROSCUSTOS  = outros ÷ (base + II + IPI + PIS + COFINS + aduaneira + AFRMM) × 100
CUSTOULTPEDCOMPRA = PCOMPRA × COT + II + aduaneira + outros custos + frete EM USD, SEM converter
VLTOTAL           = Σ arred2(QT × parcela gravada): base, II, IPI, PIS, COFINS, aduaneira, AFRMM
                    (11841: 321.503,27 exato; somar sem arredondar cada parcela daria ,29)
```
- **O custo leva o frete em dólar sem converter e não leva o AFRMM.** Parece
  **erro da 3010**, a mesma mistura de moeda do CUSTOREP (03_VALIDACOES/EVIDENCIAS_TRACE_E_BANCO.md). A aplicação
  replica (decisão 4: igual à 3010). **Avisar o time**; se decidirem corrigir,
  é uma linha em `calcularValoresItem`.
- **Implementado:** `calculo/despesas.calculo.ts` (`ratearDespesas`, com o
  AFRMM de 10%), as despesas em `calcularValoresItem` (valores, percentuais,
  custo novo) e o VLTOTAL com o arredondamento da tela. A 9ª rodada confere
  os 7 pedidos pelo cálculo novo (2.17).
- **Para a tela (etapa 2):** o pedido recebe frete (USD), despesa aduaneira
  (R$) e outros custos (R$), e o AFRMM sai calculado. Continua sem se saber
  **onde a 3010 guarda esses totais** e se o AFRMM é digitado ou calculado
  (7 de 7 = 10%). **O trace de um lançamento com despesas responde os dois.**
- **3.6:** a prévia deu 503 (o comex não respondeu ou recusou). O roteiro
  agora mostra a mensagem. Suspeita: comex-api no ar sem o patch da rota
  `/leitura` (`comex-api-rota-leitura.patch`), o que daria 404.

## Homologação, 9ª rodada (24/09): o cálculo novo nos 7 pedidos

- **VLTOTAL:** a busca do 2.20 achou sozinha, nos 11 primeiros pedidos,
  `VLTOTAL = Σ QT × (base + impostos) + Σ(QT×VLADUANEIRA) + Σ(QT×VLAFRMM)`.
  O 2.17 bate **exato** em 11841, 11840 e nos 4 sem frete. Nos outros 5 ficou
  a 10 a 27 centavos.
- **AFRMM, erro meu, CORRIGIDO (com teste):** o gravado é 10% do frete em reais
  **sem os centavos** (11839: 11.812,00, não 11.812,11; 11831: 656, não
  656,23). Derivar 10% exato errava 5 de 7 pedidos na 5ª casa. Agora o AFRMM
  é **total informado**, com `sugerirAfrmm` (10% sem centavos) como sugestão
  para a tela. Corta ou o time digita redondo? Os centavos ficaram todos
  abaixo de 0,50, então não dá para saber: o trace dirá.
- **Estimativa dos totais no roteiro, CORRIGIDA (com teste):** sem saber onde
  a 3010 guarda os totais, o roteiro somava os itens e arredondava. No 11833
  isso dá 1.238,16, e o total dos pedidos irmãos é 1.238,17. Agora
  `estimarTotal` testa ±1 e ±2 centavos e fica com o total que reproduz os
  itens.
- **3.6: o comex respondeu 405 (Method Not Allowed) no `POST /leitura`.** O
  comex-api no ar **não tem o patch** da rota: sem ele, o caminho cai numa
  rota de outro método. Aplicar `comex-api-rota-leitura.patch` no comex e
  reiniciar.

## Homologação, 10ª rodada (24/09): o que sobra são os totais digitados

- **23 de 43** itens com frete batem em tudo. **11838 e 11839: todos os itens
  iguais**; só o VLTOTAL fica a 1 ou 2 centavos. 11841 e 11840 batem inteiros.
- **Nos 11831 a 11833 o frete foi digitado em REAIS.** O 11832 tem 1 item com
  500 un e VLFRETE gravado 2,476332 → 1.238,166 USD, que não é centavo de dólar,
  = **6.562,28 R$ ÷ 5,30**. O AFRMM 656 é 10% de 6.562,28 sem os centavos.
  O roteiro estimava o frete em dólar (1.238,17) e errava a 6ª casa.
  Corrigido com teste: `melhorTotalDoFrete` testa dólar e reais.
  **Para a tela:** o frete pode ser digitado em reais (ou nas duas moedas):
  o trace confirma.
- **VLTOTAL do 11838 e do 11839:** com todos os itens iguais, a diferença de
  centavos só pode ser o arredondamento do total, provado até agora só no
  11841. O item novo **2.22** testa as formas de arredondar com os valores
  GRAVADOS, que não dependem de estimativa.
- **11833:** o valor por kg não é igual em todos os itens. O 2.17 passa a
  contar os itens do pedido fora da comparação (base zerada), que podem estar
  entrando no rateio.
- **3.6 continua 405:** o patch do comex ainda não foi aplicado.

## Homologação, 11ª rodada (24/09): itens quase todos, o VLTOTAL por centavos

- **Itens:** 25 de 43 com frete iguais; só o 11833 ainda difere. O PERCFRETE
  calculado é sempre 0,999995 do gravado, então o frete real é 1.238,166 USD =
  **6.562,28 R$** (o mesmo dos irmãos). Os dois totais reproduzem o VLFRETE na
  6ª casa, e só o PERCFRETE distingue. **Corrigido com teste:** a estimativa
  conta o PERCFRETE e a faixa de busca cresce com a quantidade (em reais, ±2
  centavos não alcançavam).
- **VLTOTAL (2.22, valores gravados): nenhuma forma simples bate nos 11.**
  "Parcela × QT a 2 casas" bate em 7 (erra 11839, 11838, 11833, 11832).
  "Soma sem arredondar" bate em 7 (erra 11841, 11840, 11835, 11832). As duas se
  complementam, e o 11832 não bate em nenhuma. Hipótese: a tela soma com os
  valores **internos**, antes de gravar as 6 casas. O 2.17 passa a mostrar o
  VLTOTAL com os valores internos do cálculo (parcela × QT e soma).
  **Se isso também não fechar**, o VLTOTAL do 1º pedido fica com a regra de
  "parcela × QT" e uma diferença conhecida de até 2 centavos. É decisão do
  time se isso importa: o contas a pagar nasce do 2º pedido (03_VALIDACOES/EVIDENCIAS_TRACE_E_BANCO.md).

## Homologação, 12ª rodada (24/09): CÁLCULO DO 1º PEDIDO FECHADO

```
itens:   sem frete 28 de 28 · com frete 43 de 43 → 71 de 71 iguais em tudo
         (base, II, IPI, PIS, COFINS, custo, frete, despesa aduaneira, outros
          custos, AFRMM e os percentuais)
VLTOTAL: 8 de 11 exatos · 11839 −0,02 · 11838 −0,01 · 11833 +0,01
```
Nem os valores internos fecham os 3 restantes: cada forma de somar acerta uns e
erra outros. É arredondamento da própria tela. **Decisão (01_ARQUITETURA/DECISOES.md): até 2
centavos aceitos.** O roteiro separa "exato" de "a até 2 centavos".

**Resumo do que o cálculo cobre, provado contra a homologação:** 1º pedido sem
frete; com frete (digitado em USD ou em R$), despesa aduaneira, outros custos e
AFRMM, tudo repartido por PESOLIQDI × QT; custo com o frete em USD sem
converter (a mistura de moeda da 3010, replicada; **avisar o time**).
**Não cobre:** seguro, capatazia, Siscomex (só vistos em 2º pedido), redução
de base, IPI por valor. Pedido com esses campos vira caso de teste antes.

**Para a gravação (etapa 3), ainda em aberto:** onde a 3010 guarda os totais
das despesas, em que moeda o time digita o frete, e se o AFRMM é digitado ou
calculado (10% sem centavos). O trace de um lançamento com despesas responde.

## Homologação, 17ª rodada (24/09): O BACKEND INTEIRO VALIDADO

**21 ok · 0 erro · 0 pulado.** Pela primeira vez o caminho inteiro rodou contra
a MIMO-HOMOLOG: login WinThor (setor 18), filiais pela PCLIB, cotação, impostos
e **a prévia com um LAST de verdade**:
```
26MZC289F → comex (/leitura) → de-para no WinThor → regras → prévia
  3 itens · podeGravar false
  Linha 8: código BH26081, descrição começa com BH26082   ← o erro que a PROCESSOS confirmou
  Linha 9: código BH26082, descrição começa com BH26081
  pedidos da 3010 com a mesma invoice: nenhum
```
- **comex-api:** o patch da rota `/leitura` entrou (commit no repositório do
  comex, 5 testes passando). O teste lê a senha dos LASTs só do ambiente
  (`PLANILHA_SENHA`); a senha padrão que o teste tinha saiu antes do push.
  O comex precisa subir com a `PLANILHA_SENHA` exportada no mesmo terminal
  e em `127.0.0.1`.
- **Os 6 "diferente" que sobram são conhecidos:** 1.6 (porto do 9726,
  resolvido: nacionalização), 1.10 (cotação de 2105, dado da base), 1.13
  (numerador da homologação atrás, dado da base; a gravação confere o master),
  2.11 (planilha do time com erros de digitação e duplicados "MP" da família
  HTC, que viram pendência), 2.14 (II 14,4 do 11849, que é 2º pedido com o II
  da DI) e 2.21 (respondido: o 1º pedido tem frete).
- Nome de LAST com **espaço não separável** (o `ls -b` mostra sem a barra):
  digitar o nome não funciona; usar curinga (`ls ../lasts/26MZC289F*`).

## Homologação, 18ª rodada (30/09): QTSUGESTAO FECHADA

Rodada focada contra a base TESTE, em transação somente leitura, já com o código
final `b813ceb`:

```text
NUMPED_QTSUGESTAO=11866 API_URL=nao npm run homologacao

16 ok · 5 diferente · 0 erro · 17 info · 2 pulado
```

O pedido **11866** foi lançado manualmente pela própria rotina 3010, filial 4,
fornecedor 15. O item 2.24 reproduziu a `QTSUGESTAO` em **2 de 2 itens**:

```text
8360   1 × (150 + 21) - 925 = -754
11190  10 × (150 + 21) - 0 = 1710
```

Resultado do roteiro:

```text
pedido 11866 · 2 item(ns) · pendente não considerado ·
conta-base reproduz 2/2
```

A regra fechada para o caminho homologado é:

```text
QTSUGESTAO =
    PCEST.QTGIRODIA
    × (PCFORNEC.PRAZOENTREGA + PCPRODUT.TEMREPOS)
    - PKG_ESTOQUE.ESTOQUE_DISPONIVEL(CODPROD, CODFILIAL, 'C')
```

O resultado negativo é preservado. Testes manuais na própria
PCSIS3010 v37.0.08.071 também mostraram que `QTVEZES` não altera a conta-base
observada e que prazo/tempo de reposição positivos informados na tela substituem
os valores de cadastro.

A filial 4 possui `CONSIDERAESTPENDSUGCOMPRA='N'`. A TESTE não forneceu caso
com `'S'`; por isso esse ramo continua não homologado e a API o recusa.

Os **5 DIFERENTE** desta rodada pertencem às verificações já conhecidas do
roteiro e não representam regressão da `QTSUGESTAO`.

Código relacionado:

```text
c96e389  fix: usa PCEST na validacao da QTSUGESTAO
b813ceb  feat: calcula QTSUGESTAO como a rotina 3010
```

## Ainda não rodou de verdade (atenção)

- **CI/CD nunca rodou** no GitHub nem no runner. O `mount` no .40 também não
  (o teste usa pasta local).
- **Ganchos no Windows** (Git Bash) não testados.

## Achados na revisão do pacote (antes da etapa 2)

- **CORRIGIDO: a cotação saía do dia anterior.**
  ```
  GET /cadastros/cotacao?moeda=220&data=2026-07-19
    ↓  @Type(() => Date) → new Date('2026-07-19') = 19/07 00:00 UTC = 18/07 21:00 em Brasília
    ↓  node-oracledb 6.10 envia Date como TIMESTAMP com a hora LOCAL
    ↓  Oracle recebia 18/07 21:00 → TRUNC → 18/07
    ↓  voltava a cotação de 18/07 com "data": "2026-07-19"
  ```
  E `data=2026-02-30` era aceita: o `new Date` empurrava para 02/03 e a rota
  consultava 01/03 sem avisar. Correção: a data fica texto `AAAA-MM-DD`
  (validado: formato e calendário) e vira data no Oracle com
  `TO_DATE(:2, 'YYYY-MM-DD')`, sem depender do fuso do servidor. Teste de
  regressão em `test/cotacao.e2e-spec.ts`; o apoio `test/apoio/data-no-oracle.ts`
  usa o codificador do próprio driver para mostrar o que chega no Oracle.
  **Regra para a etapa 3:** nenhuma data vai para o Oracle como Date do
  JavaScript; sempre texto + `TO_DATE`. Conferir com
  `diaComparadoNaConsulta` / `dataQueOOracleRecebe`.
- **FEITO: regra D na prévia.** Cada pedido da prévia traz
  `pedidosComMesmaInvoice`: os pedidos do WinThor com o mesmo
  `PCPEDIDO.NUMINVOCE` (NUMPED, IDPEDIDOMASTER, CODFORNEC, fornecedor,
  negociação, emissão, quem lançou, rotina). **Não trava a prévia**, porque o
  fornecedor só é escolhido depois: a tela compara com o CODFORNEC escolhido e,
  se bater, pede o motivo; a gravação confere de novo. Uma consulta só para o
  lote (`winthor/pedidos-da-invoice.oracle.ts`). Decisões de implementação:
  compara só NUMINVOCE (NUMPROFORMA daria alarme falso com a sobra do pedido
  anterior); não filtra ROTINALANC (a rotina vem na resposta); emissão sai
  como texto (TO_CHAR). Teste com o caso 11840/11841 (NUMPED e invoice reais,
  fornecedor e negociação ilustrativos). **Conferir na homologação:** se
  IDPEDIDOMASTER e FUNCLANC existem no PCPEDIDO com esses nomes, e o tempo
  da consulta (`UPPER(TRIM(NUMINVOCE))` não usa índice).
- **FEITO: rota dos impostos por item.**
  `GET /cadastros/impostos?filial=4&fornecedor=15&pais=1600&porto=1&produtos=9018,15708`.
  Copia a consulta da tela (trace, entrada 237) em `winthor/impostos-item.oracle.ts`:
  os blocos TRIBUTACOES e EXCECOES têm FROM e WHERE iguais. Ligação coluna da
  consulta → PCITEM conferida nos binds do INSERT PCITEM do 11681 (mesmo nome):
  ```
  PERCIMPORTACAO 20 · PERCIPI→PERIPI 6,5 · PERPIS 2,1 · PERCOFINS 9,65 · CUSTOULTENT 862,091374
  PERPISCALCDI e PERCOFINSCALCDI = 0 → NÃO são esses que a tela usa para PIS/COFINS
  PERCICMSDIFERIDO 100 e PERICM 0 → por isso não há ICMS no cálculo
  ```
  Cada filtro que faria a 3010 esconder o produto na grade vira **restrição**
  com o motivo (sem tributação, sem PCEST/PCPRODFILIAL na filial, sem preço na
  região, fora de linha, proibido para venda, TIPOMERC CB, sem departamento).
  Campo do cadastro diferente do único caso conferido pelo cálculo (seguro,
  frete, IPI por valor, ICMS, suspensão...) aparece em **foraDoCalculo**.
  `podeUsar` só é true sem nenhum dos dois. **Conferir na homologação** (a
  rota devolve tudo isso para comparar):
  - `numRegiao`: hipótese de que o `:NUMREGIAO` 300 da tela é o
    `PCFILIAL.NUMREGIAOPADRAO` da filial 4;
  - país e porto: no trace, origem = procedência = aquisição = 1600 e
    chegada = nacionalização = 1. Hipótese: a tela usa origem e chegada;
  - `parametrosDaTela` (TIPOTRIBENTIMP e CON_USATRIBUTACAOPORUF): a consulta
    copiada é a do caminho que a tela seguiu com os valores desta base;
  - 9018, filial 4, fornecedor 15, China, porto 1 deve voltar 20 / 6,5 / 2,1 / 9,65.
- **CORREÇÃO do 03_VALIDACOES/EVIDENCIAS_TRACE_E_BANCO.md: o INSERT PCFORNECFILIAL da tela é de TODOS os
  fornecedores.** Trace, entradas 190 a 192: `INSERT ... SELECT` de PCFORNEC ×
  PCFILIAL onde falta, fora a filial 99, **sem filtro de fornecedor e sem
  parâmetro**, com COMMIT na hora, antes de o pedido existir. Por isso a rota
  não trata "fornecedor fora da filial" como restrição. Pesa na decisão 4 para
  a etapa 3 (item 10 dos pontos em aberto (00_STATUS)).
- **FEITO: rota da regra A.** `GET /cadastros/negociacao/validar?valor=26603&invoice=26MMC709F`
  devolve `{ valor, nivel: ok | aviso | bloqueio, mensagem, podeSeguir }`, sem
  consultar o banco. Usa a mesma `validarNumNegociacao` que a gravação vai
  usar. Devolve o `valor` como foi enviado, para a tela descartar resposta
  atrasada enquanto o usuário digita. Testes em `test/negociacao.e2e-spec.ts`.
- Gancho de commit: um `git commit --amend` num commit de correção é
  recusado se o que se acrescenta não tem teste, mesmo que o commit original
  tenha. O gancho olha só o que está sendo acrescentado. Contornar com commit
  separado, nunca com `--no-verify`.
- Miudezas: comentário desatualizado em `previa.service.ts` (diz que a regra
  do NUMINVOCE e do NUMNEGOCIACAO está em aberto); eslint com 142 erros (125
  só de formatação) e o CI não roda o eslint.

---
