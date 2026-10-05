# Validação — Evidências do trace da 3010 e do banco

**Natureza:** evidência. O que o trace da própria 3010 (pedido 11681,
`TRACE3010_-_PEDIDO_MASTER_2.log`) e as consultas no banco mostraram. É a base
das regras de `02_FLUXOS/`: quando uma regra diz "como a 3010", a prova está
aqui. Migrado do §5 do antigo `CONTINUAR.md`.

**Sequência da gravação na tela (trace do pedido 11681):**
```
1. SELECT ... PCCONSUM FOR UPDATE → UPDATE PROXNUMPED + 1        → COMMIT na hora
2. SELECT ... PCNUMERADORIMP FOR UPDATE → UPDATE PROXNUMPEDIDO + 1 → COMMIT na hora
   (a própria 3010 queima número se o usuário desistir)
3. INSERT PCFORNECFILIAL de TODOS os fornecedores em todas as filiais que
   faltam (fora a 99), sem parâmetro   → COMMIT na hora  (ver VALIDACAO_HOMOLOGACAO_RODADAS)
4. transação única:
   DELETE PCPEDIDO / PCITEM / PCCONTAINERS do NUMPED
   INSERT PCITEM  →  INSERT PCPEDIDO
   UPDATE PCFORNEC (TIPOEMBALAGEMPEDIDO)
   UPDATE PCPRODUT (CUSTOREP = PCOMPRA em dólar, sem converter; datas e usuário)
   UPDATE PCPRODFILIAL (PERCALTERCUSTOENT)
   COMMIT
```
Há um gatilho `TRG_PCITEMLOG` no PCITEM. O trace corta em 100 valores por
comando; as colunas que faltaram estão na aba INSERTS do template (136 + 173).

**Cálculos (por unidade, item 9018: 83,74 USD, cotação 5,30):**
```
base (BASEPISCOFINSLIT)          = 83,74 × 5,30                 = 443,822
II   (VLIMPORTACAO)              = base × 20%                   = 88,7644
PIS  (VLCREDPIS)                 = base × 2,1%                  = 9,320262
COFINS (VLCREDCOFINS)            = base × 9,65%                 = 42,828823
IPI  (VLIPI)                     = (base + II) × 6,5%           = 34,618116
CUSTOULTPEDCOMPRA / ...SEMST     = base + II                    = 532,5864
VLTOTAL (pedido)                 = Σ qtd × (base+II+IPI+PIS+COFINS) = 619.353,60
```
Válido só com frete, seguro, capatazia e demais despesas em 0. O template em
planilha gravava esses campos como 0, e por isso fica diferente da tela.

**Consultas da tela** (copiadas para `cadastros.oracle.ts`): filiais pela
PCLIB do usuário, fornecedor de importação (`FORNECIMPORTACAO IN (6,7)` ou
`REVENDA='X'`), compradores (setor `PCCONSUM.CODSETORCOMPRADOR`), cotação
(`PCCOTACAOMOEDAC` + `PCCOTACAOMOEDAI` por data), países, portos, vias. A
consulta grande do item (34 KB, índice 237 do trace) traz os impostos de
`PCTRIBFIGURA` / `PCEXPISCOFINSITEM` e o custo de `PCEST` da filial do pedido. Copiada em
`winthor/impostos-item.oracle.ts` (ver VALIDACAO_HOMOLOGACAO_RODADAS).

**Dois pedidos por master (615 masters em 2026):** o 1º é lançado; depois a
própria 3010 cria o 2º com o mesmo master, mesmos itens e quantidades,
`PCITEM.NUMPEDMASTERORIGEM = NUMPEDPRINC = 1º pedido` e VLTOTAL diferente.
Nos dois casos conferidos, o **contas a pagar (PCLANC) nasce no mesmo dia do
2º pedido**. A aplicação cria só o 1º, com esses dois campos vazios. Não se
sabe qual ação da 3010 gera o 2º.

**NUMNEGOCIACAO:** sem numerador, sem sequência, sem gatilho (o pacote
FUNCOESCOMPRAS só copia a coluna). Formato ano + sequência: `25514` para
`25MIW189F`, `26602` para `26MMC709F`. Controlado numa planilha. Vai para
PCLANC, PCPREST, PCNFENT e PCMOV (erro chega no financeiro). Uma negociação
pode cobrir vários pedidos (26492 em 12; 26578 com 4 fornecedores no
26ALFMIMO-15). Desde agosto: 317 no padrão, 29 com 4 dígitos (padrão de
outras BUs), 57 vazios, 18 zeros.

**Código x descrição trocados (4 casos em 198 itens, confirmados pela PROCESSOS):**
26MZC289F linhas 8/9 (BH26081 ↔ BH26082), 26MQS575F linha 15 (PF26264 com
descrição do CM26266), 26MKP551F linha 5 (CE26142 com descrição do CE26141). A
invoice gerada pelo comex também carrega o erro — vale pôr a regra no comex.

**Pedidos 11840 / 11841:** mesma invoice 26MCS415F, mesmo fornecedor e mesma
negociação, com produtos diferentes. O 11841 tem proforma 26MCS400F. Os itens
do 11840 são idênticos ao 26MCS388F da PROCESSOS. Com os LASTs 388F, 400F e
415F dá para fechar.

**Rede:** `localhost` no `COMEX_API_URL` faz o Node tentar IPv6 e falhar com o
comex no ar. Usar `127.0.0.1`.

## QTSUGESTAO — trace, teste manual e banco

O trace foi útil para identificar as variáveis envolvidas, mas **não foi
suficiente para fechar a conta final**. A validação prática posterior na
PCSIS3010 v37.0.08.071 substitui a hipótese antiga que incluía `QTVEZES`.

Do trace permanece como evidência:

```text
ESTOQUE        = PKG_ESTOQUE.ESTOQUE_DISPONIVEL(CODPROD, CODFILIAL, 'C')
QTPENDENTE     existe no caminho da sugestão
QTMINSUGCOMPRA e MULTIPLOCOMPRAS são lidos
```

O pedido nativo **11866**, lançado pela própria 3010 na TESTE, fechou a
conta-base em **2 de 2 itens**:

```text
8360   1 × (150 + 21) - 925 = -754
11190  10 × (150 + 21) - 0 = 1710
```

Regra homologada para filial que não considera estoque pendente:

```text
ESTOQUE_IDEAL =
    PCEST.QTGIRODIA ×
    (PCFORNEC.PRAZOENTREGA + PCPRODUT.TEMREPOS)

QTSUGESTAO =
    ESTOQUE_IDEAL -
    PKG_ESTOQUE.ESTOQUE_DISPONIVEL(CODPROD, CODFILIAL, 'C')
```

O resultado negativo é preservado.

Teste manual direto na 3010 também mostrou que alterar
`Qt. vezes estq. ideal` de 1 para 2 **não alterou** o estoque ideal nem a
`QTSUGESTAO`. Portanto, `QTVEZES` não entra na conta-base observada neste
caminho da versão testada.

Também foram validados os campos de sobrescrita da tela:

```text
Tempo reposição = 10  -> 1 × (150 + 10) - 925 = -765
Prazo entrega = 20    -> 1 × (20 + 21) - 925 = -884
```

Com esses campos em zero, o caminho observado usa os valores de cadastro. A
aplicação atual não expõe essas sobrescritas e usa os valores cadastrados.

A base TESTE não possui filial com
`CONSIDERAESTPENDSUGCOMPRA='S'`. Por isso o tratamento de `QTPENDENTE` continua
**não homologado**. A aplicação recusa esse cenário em vez de assumir uma
fórmula.

Também não houve caso positivo útil de `QTMINSUGCOMPRA` ou
`MULTIPLOCOMPRAS` na filial 4; esses campos permanecem apenas como diagnóstico.

Detalhes, testes e critério de segurança:
`04_VALIDACOES/ROTEIRO_QTSUGESTAO.md`.

Código implementado:

```text
c96e389  fix: usa PCEST na validacao da QTSUGESTAO
b813ceb  feat: calcula QTSUGESTAO como a rotina 3010
```
