# Fluxo — Cálculo do 1º pedido do master

Os valores de cada PCITEM e o VLTOTAL do PCPEDIDO, calculados como a 3010 grava.
Regras **deduzidas da homologação e conferidas até a 6ª casa** (rodadas 8ª a
12ª, `04_VALIDACOES/VALIDACAO_HOMOLOGACAO_RODADAS.md`); implementadas em
`api/src/modules/calculo/` e cobertas por teste com pedidos reais como fixture.

```text
71 de 71 itens iguais à homologação
VLTOTAL a até 2 centavos (decisão de 24/09: 8 de 11 exatos; 3 a 1-2 centavos,
        arredondamento da própria tela; o contas a pagar nasce do 2º pedido)
```

## 1. Sem frete (o que a gravação usa hoje)

Por unidade, com os percentuais do cadastro tributário (exemplo do trace,
item 9018: 83,74 USD, cotação 5,30):

```text
base (BASEPISCOFINSLIT)        = PCOMPRA × COT                = 443,822
II   (VLIMPORTACAO)            = base × %II                   = 88,7644      (20%)
PIS  (VLCREDPIS)               = base × %PIS                  = 9,320262     (2,1%)
COFINS (VLCREDCOFINS)          = base × %COFINS               = 42,828823    (9,65%)
IPI  (VLIPI)                   = (base + II) × %IPI           = 34,618116    (6,5%)
CUSTOULTPEDCOMPRA / ...SEMST   = base + II                    = 532,5864
```

```text
VLTOTAL = Σ arred2(QT × parcela), parcela por parcela: base, II, IPI, PIS, COFINS
          (11681: 619.353,60; 11858: 84.059,54)
```

## 2. Com frete e despesas (calculado, ainda não gravado)

Fixture real: 1º pedido 11841 (`api/test/fixtures/homologacao-11841-despesas.json`).

```text
os totais do pedido são repartidos por PESOLIQDI × QT (por unidade, sem arredondar):
  frete (USD ou R$) · despesa aduaneira (R$) · outros custos (R$) · AFRMM (R$)
AFRMM             = o total informado; a sugestão é 10% do frete em reais SEM os centavos
                    (visto nos 7 pedidos da homologação)
base              = (PCOMPRA + frete) × COT          -> II, PIS, COFINS, IPI como no item 1
PERCADUANEIRA, PERCAFRMM = despesa ÷ base × 100
PERCOUTROSCUSTOS  = outros ÷ (base + II + IPI + PIS + COFINS + aduaneira + AFRMM) × 100
CUSTOULTPEDCOMPRA = PCOMPRA × COT + II + aduaneira + outros custos + frete EM USD, sem converter
VLTOTAL           = Σ arred2(QT × parcela): base, II, IPI, PIS, COFINS, aduaneira, AFRMM
                    (11841: 321.503,27 exato)
```

**O custo leva o frete em dólar sem converter** e não leva o AFRMM. Parece
**erro da 3010** (a mesma mistura de moeda do CUSTOREP); a aplicação replica
(decisão 4: igual à 3010). **Avisar o time**; se decidirem corrigir, é uma linha
em `calcularValoresItem`.

**Não cobre:** seguro, capatazia, Siscomex (só vistos em 2º pedido), redução de
base, IPI por valor. Pedido com esses campos vira caso de teste antes.

## 3. Rota

```text
POST /api/v1/calculo/pedido       calcula, não grava
```

Recebe os itens (CODPROD, QT, PCOMPRA, percentuais), a cotação e os totais do
pedido; devolve os valores por item (como o PCITEM), o VLTOTAL e as pendências
(item sem PESOLIQDI com despesa vira pendência: o rateio recusa repartir sem
peso). Contrato em `05_CONTRATOS/CONTRATO_API_PEDIDO_3010.md`.

## 4. Peso (PESOLIQDI)

Desde a validação do time (25/09), o peso de cada item é o **N.W. da linha do
LAST ÷ quantidade**, 6 casas; o cadastro só quando o LAST não traz o peso. É o
peso usado no rateio das despesas e o que vai para o PCITEM (e, pelo bloco da
3010, para o PCPRODUT). Ver `02_FLUXOS/GRAVACAO_NA_3010.md`.

## 5. Em aberto para gravar com frete

Onde a 3010 guarda os totais das despesas, em que moeda o time digita o frete e
se o AFRMM é digitado ou calculado. **Um trace de um lançamento com despesas
responde.**
