# Contrato — As 309 colunas que a 3010 grava (PCITEM e PCPEDIDO)

**Natureza:** contrato de gravação, coberto por teste. Para cada coluna: o
valor que a 3010 gravou no pedido 11681 (trace), o valor que o template gera
para o mesmo pedido, a origem segundo a aba LEIA-ME e se os dois conferem.

A montagem da API (`api/src/modules/gravacao/colunas-3010.ts`) foi **gerada
desta tabela** e o teste de ouro (`montagem.spec.ts`) prova que ela reproduz o
template nas 309 colunas e o trace nas 200 que ele mostra. Detalhes do
cruzamento em `03_VALIDACOES/VALIDACAO_TEMPLATE_X_TRACE.md`.

O trace corta em 100 valores por comando: "só template" são as colunas depois
do corte, que só o template tem.

> **Nota sobre QTSUGESTAO (30/09/2026):** a linha da tabela mantém de propósito
> a comparação histórica do pedido 11681 (`trace = -2316`, `template = 0`).
> Ela não representa mais o comportamento atual da aplicação. A `QTSUGESTAO`
> foi homologada depois com o pedido nativo 11866 e passou a ser calculada na
> gravação; ver `03_VALIDACOES/ROTEIRO_QTSUGESTAO.md`.

## PCITEM: 173 colunas

| # | Coluna | 11681 (trace) | Template | Origem (LEIA-ME) | Confere |
|---|---|---|---|---|---|
| 1 | `NUMPED` | 11681.000000 | v_ped('P1') | PCCONSUM.PROXNUMPED (FOR UPDATE NOWAIT + 1) · PCPEDIDO | **diferente** |
| 2 | `NUMSEQ` | 1 | 1 | automatico: 1, 2, 3... por pedido · PCITEM | igual |
| 3 | `CODPROD` | 9018.000000 | 9018 | Numero inteiro · B | igual |
| 4 | `QTPEDIDA` | 1000.000000 | 1000 | Decimal (6 casas) · C | igual |
| 5 | `PCOMPRA` | 83.740000 | 83.74 | Decimal (6 casas) · D | igual |
| 6 | `PLIQUIDO` | 83.740000 | 83.74 | Decimal (6 casas) · E | igual |
| 7 | `PERIPI` | 6.500000 | 6.5 | Decimal (2 casas) · F · vazio = 6.5 | igual |
| 8 | `PERPIS` | 2.100000 | 2.1 | Decimal (2 casas) · G · vazio = 2.1 | igual |
| 9 | `PERCOFINS` | 9.650000 | 9.65 | Decimal (2 casas) · H · vazio = 9.65 | igual |
| 10 | `PERCIMPORTACAO` | 20.000000 | 20 | Decimal (2 casas) · I · vazio = 20 | igual |
| 11 | `PERCICMSDIFERIDO` | 100.000000 | 100 | Decimal (2 casas) · J · vazio = 100 | igual |
| 12 | `CODSITTRIBPISCOFINS` | 50.000000 | 50 | Numero inteiro · K · vazio = 50 | igual |
| 13 | `PESOLIQDI` | — | 27.1 | Decimal (6 casas) · L · vazio = 27.1 | só template |
| 14 | `CUSTOULTENT` | 862.091374 | (SELECT NVL(MAX(CUSTOULTENT),0) FROM PCEST WHERE CODPROD = 9018 AND CODFILIAL = '4') | PCEST.CUSTOULTENT do CODPROD na CODFILIAL do pedido · PCITEM | **diferente** |
| 15 | `QTSUGESTAO` | -2316.000000 | 0 | Decimal (6 casas) · N · vazio = 0 | **diferente** |
| 16 | `CODPRODORIGEM` | — | 9018 | igual a CODPROD · PCITEM | só template |
| 17 | `CODFUNCALTER` | — | 349 | CODFUNC do pedido (VLOOKUP pela CHAVE) · PCITEM | só template |
| 18 | `BASEPISCOFINSLIT` | 443.822000 | 443.822 | PLIQUIDO x COTACAO · 83,74 x 5,30 = 443,822 | igual |
| 19 | `VLIMPORTACAO` | 88.764400 | 88.7644 | BASE x PERCIMPORTACAO · 443,822 x 20% = 88,7644 | igual |
| 20 | `CUSTOULTPEDCOMPRA` | — | 532.5864 | BASE x (1 + PERCIMPORTACAO) · 443,822 x 1,20 = 532,5864 | só template |
| 21 | `CUSTOULTPEDCOMPRASEMST` | — | 532.5864 | igual ao CUSTOULTPEDCOMPRA · 532,5864 | só template |
| 22 | `VLIPI` | 34.618116 | 34.618116 | CUSTOULTPEDCOMPRA x PERIPI · 532,5864 x 6,5% = 34,618116 | igual |
| 23 | `VLCREDPIS` | 9.320262 | 9.320262 | BASE x PERPIS · 443,822 x 2,1% = 9,320262 | igual |
| 24 | `VLCREDCOFINS` | 42.828823 | 42.828823 | BASE x PERCOFINS · 443,822 x 9,65% = 42,828823 | igual |
| 25 | `BASEICMS` | 0.000000 | 0 | 0 · PCITEM | igual |
| 26 | `PERICM` | 0.000000 | 0 | 0 · PCITEM | igual |
| 27 | `PERCDESC` | 0.000000 | 0 | 0 · PCITEM | igual |
| 28 | `PERCDESC1` | 0.000000 | 0 | 0 · PCITEM | igual |
| 29 | `PERCDESC2` | 0.000000 | 0 | 0 · PCITEM | igual |
| 30 | `PERCDESC3` | 0.000000 | 0 | 0 · PCITEM | igual |
| 31 | `PERCDESC4` | 0.000000 | 0 | 0 · PCITEM | igual |
| 32 | `PERCDESC5` | 0.000000 | 0 | 0 · PCITEM | igual |
| 33 | `PERCDESC6` | 0.000000 | 0 | 0 · PCITEM | igual |
| 34 | `PERCDESC7` | 0.000000 | 0 | 0 · PCITEM | igual |
| 35 | `PERCDESC8` | 0.000000 | 0 | 0 · PCITEM | igual |
| 36 | `PERCDESC9` | 0.000000 | 0 | 0 · PCITEM | igual |
| 37 | `PERCDESC10` | 0.000000 | 0 | 0 · PCITEM | igual |
| 38 | `PERCCREDICMPRESUMIDO` | 0.000000 | 0 | 0 · PCITEM | igual |
| 39 | `PERCOUTRASDESP` | 0.000000 | 0 | 0 · PCITEM | igual |
| 40 | `PERCICMRED` | 0.000000 | 0 | 0 · PCITEM | igual |
| 41 | `QTENTREGUE` | 0.000000 | 0 | 0 · PCITEM | igual |
| 42 | `PERCFRETE` | 0.000000 | 0 | 0 · PCITEM | igual |
| 43 | `VLPAUTA` | 0.000000 | 0 | 0 · PCITEM | igual |
| 44 | `PERCFRETEFOB` | 0.000000 | 0 | 0 · PCITEM | igual |
| 45 | `VLFRETE` | 0.000000 | 0 | NULL · PCPEDIDO | igual |
| 46 | `VLOUTRASDESP` | 0.000000 | 0 | 0 · PCITEM | igual |
| 47 | `NUMADICAO` | 0.000000 | 0 | 0 · PCITEM | igual |
| 48 | `NUMSEQADICAO` | 0.000000 | 0 | 0 · PCITEM | igual |
| 49 | `PERCDESCICMSDIF` | 0.000000 | 0 | 0 · PCITEM | igual |
| 50 | `PERCIISUSPENSO` | 0.000000 | 0 | 0 · PCITEM | igual |
| 51 | `PERCOFINSCALCDI` | 0.000000 | 0 | 0 · PCITEM | igual |
| 52 | `PERPISCALCDI` | 0.000000 | 0 | 0 · PCITEM | igual |
| 53 | `UTILIZACREDREDPISCOFINS` | 'N' | 'N' | 'N' · PCITEM | igual |
| 54 | `REDBASEIVA` | 0.000000 | 0 | 0 · PCITEM | igual |
| 55 | `REDBASEALIQEXT` | 0.000000 | 0 | 0 · PCITEM | igual |
| 56 | `PERICMSANTECIPADO` | 0.000000 | 0 | 0 · PCITEM | igual |
| 57 | `PERCIVA` | 0.000000 | 0 | 0 · PCITEM | igual |
| 58 | `PERCALIQINT` | 0.000000 | 0 | 0 · PCITEM | igual |
| 59 | `PERCALIQEXT` | 0.000000 | 0 | 0 · PCITEM | igual |
| 60 | `TIPOCALCST` | 'N' | 'N' | 'N' · PCITEM | igual |
| 61 | `PERCDESPADICIONAL` | 0.000000 | 0 | 0 · PCITEM | igual |
| 62 | `PRODBONIFICADO` | 'N' | 'N' | 'N' · PCITEM | igual |
| 63 | `VLST` | 0.000000 | 0 | 0 · PCITEM | igual |
| 64 | `VLDESPADICIONAL` | 0.000000 | 0 | 0 · PCITEM | igual |
| 65 | `VLICMSANTECIPADO` | 0.000000 | 0 | 0 · PCITEM | igual |
| 66 | `PERCALIQEXTGUIA` | 0.000000 | 0 | 0 · PCITEM | igual |
| 67 | `CALCCREDIPI` | 'S' | 'S' | 'S' · PCITEM | igual |
| 68 | `APROVEITACREDICMS` | 'N' | 'N' | 'N' · PCITEM | igual |
| 69 | `APROVEITACREDPISCOFINS` | 'S' | 'S' | 'S' · PCITEM | igual |
| 70 | `VLICMS` | 0.000000 | 0 | 0 · PCITEM | igual |
| 71 | `PERCREDICMS` | 0.000000 | 0 | 0 · PCITEM | igual |
| 72 | `VLCREDICMS` | 0.000000 | 0 | 0 · PCITEM | igual |
| 73 | `DTEMISSAOLICENCAIMP` | Null | NULL | NULL · PCITEM | igual |
| 74 | `DTVALIDADELICENCAIMP` | Null | NULL | NULL · PCITEM | igual |
| 75 | `NUMLICENCAIMPORT` | Null | NULL | NULL · PCITEM | igual |
| 76 | `VLPAUTAPISCOFINS` | 0.000000 | 0 | 0 · PCITEM | igual |
| 77 | `USAPISCOFINSLIT` | 'N' | 'N' | 'N' · PCITEM | igual |
| 78 | `IPIPORVALOR` | 'N' | 'N' | 'N' · PCITEM | igual |
| 79 | `VLADICIONALBCST` | 0.000000 | 0 | 0 · PCITEM | igual |
| 80 | `PERCDIREITOSADUANEIROS` | 0.000000 | 0 | 0 · PCITEM | igual |
| 81 | `PERCIMPOSTOCONSUMO` | 0.000000 | 0 | 0 · PCITEM | igual |
| 82 | `PERCIMPOSTOSELO` | 0.000000 | 0 | 0 · PCITEM | igual |
| 83 | `VLADUANEIRA` | 0.000000 | 0 | 0 · PCITEM | igual |
| 84 | `VLSISCOMEX` | 0.000000 | 0 | 0 · PCITEM | igual |
| 85 | `VLOUTRASDESPIMP` | 0.000000 | 0 | 0 · PCITEM | igual |
| 86 | `VLSEGURO` | 0.000000 | 0 | 0 · PCITEM | igual |
| 87 | `PERCSEGURO` | 0.000000 | 0 | 0 · PCITEM | igual |
| 88 | `VLDESPDENTRONF` | 0.000000 | 0 | 0 · PCITEM | igual |
| 89 | `PERCDESPDENTRONF` | 0.000000 | 0 | 0 · PCITEM | igual |
| 90 | `PERCOUTROSCUSTOS` | 0.000000 | 0 | 0 · PCITEM | igual |
| 91 | `VLOUTROSCUSTOS` | 0.000000 | 0 | 0 · PCITEM | igual |
| 92 | `PERCCAPATAZIA` | 0.000000 | 0 | 0 · PCITEM | igual |
| 93 | `VLCAPATAZIA` | 0.000000 | 0 | 0 · PCITEM | igual |
| 94 | `PERCDESPFIN` | 0.000000 | 0 | 0 · PCITEM | igual |
| 95 | `VLPAUTAICMS` | 0.000000 | 0 | 0 · PCITEM | igual |
| 96 | `PISCOFINSRETIDO` | 'N' | 'N' | 'N' · PCITEM | igual |
| 97 | `PERCST` | 0.000000 | 0 | 0 · PCITEM | igual |
| 98 | `VLBASESTGUIA` | 0.000000 | 0 | 0 · PCITEM | igual |
| 99 | `VLFRETEPORKG` | 0.000000 | 0 | 0 · PCITEM | igual |
| 100 | `VLFRETECONHEC` | 0.000000 | 0 | 0 · PCITEM | igual |
| 101 | `ROTINALANC` | 3010.000000 | 3010 | 3010 · PCPEDIDO | igual |
| 102 | `BASEICST` | 0.000000 | 0 | 0 · PCITEM | igual |
| 103 | `PERCSISCOMEX` | 0.000000 | 0 | 0 · PCITEM | igual |
| 104 | `PERCADUANEIRA` | 0.000000 | 0 | 0 · PCITEM | igual |
| 105 | `PERCOUTRASDESPIMP` | 0.000000 | 0 | 0 · PCITEM | igual |
| 106 | `PERCFRETENFCUSTO` | — | 0 | 0 · PCITEM | só template |
| 107 | `VLFRETENFCUSTO` | — | 0 | 0 · PCITEM | só template |
| 108 | `PERCSEGUROCUSTO` | — | 0 | 0 · PCITEM | só template |
| 109 | `VLSEGUROCUSTO` | — | 0 | 0 · PCITEM | só template |
| 110 | `PERCCAPATAZIACUSTO` | — | 0 | 0 · PCITEM | só template |
| 111 | `VLCAPATAZIACUSTO` | — | 0 | 0 · PCITEM | só template |
| 112 | `PERCDESPDENTRONFCUSTO` | — | 0 | 0 · PCITEM | só template |
| 113 | `VLDESPDENTRONFCUSTO` | — | 0 | 0 · PCITEM | só template |
| 114 | `VLCREDPRESUMIDO` | — | 0 | 0 · PCITEM | só template |
| 115 | `NUMDRAWBACK` | — | NULL | NULL · PCITEM | só template |
| 116 | `PERCSISCOMEXCUSTO` | — | 0 | 0 · PCITEM | só template |
| 117 | `VLSISCOMEXCUSTO` | — | 0 | 0 · PCITEM | só template |
| 118 | `PERCADUANEIRACUSTO` | — | 0 | 0 · PCITEM | só template |
| 119 | `VLADUANEIRACUSTO` | — | 0 | 0 · PCITEM | só template |
| 120 | `PERCOUTRASDESPIMPCUSTO` | — | 0 | 0 · PCITEM | só template |
| 121 | `VLOUTRASDESPIMPCUSTO` | — | 0 | 0 · PCITEM | só template |
| 122 | `PERCOUTROSCUSTOSCUSTO` | — | 0 | 0 · PCITEM | só template |
| 123 | `VLOUTROSCUSTOSCUSTO` | — | 0 | 0 · PCITEM | só template |
| 124 | `BASEICMSANTECIPADO` | — | 0 | 0 · PCITEM | só template |
| 125 | `BASECREDPRESUMIDO` | — | 0 | 0 · PCITEM | só template |
| 126 | `CALCCREDIPICONT` | — | 'S' | 'S' · PCITEM | só template |
| 127 | `APROVEITACREDICMSCONT` | — | 'N' | 'N' · PCITEM | só template |
| 128 | `APROVEITACREDPISCOFINSCONT` | — | 'S' | 'S' · PCITEM | só template |
| 129 | `GERABASEPISCOFINSSEMALIQ` | — | 'N' | 'N' · PCITEM | só template |
| 130 | `PERCICMSBASEICMSANTECIPADO` | — | 0 | 0 · PCITEM | só template |
| 131 | `VLBASEIPISUSPENSO` | — | 0 | 0 · PCITEM | só template |
| 132 | `PERCIPISUSPENSO` | — | 0 | 0 · PCITEM | só template |
| 133 | `VLIPISUSPENSO` | — | 0 | 0 · PCITEM | só template |
| 134 | `PERCALTERCUSTOENT` | — | 0 | 0 · PCITEM | só template |
| 135 | `VLIISUSPENSO` | — | 0 | 0 · PCITEM | só template |
| 136 | `CONSIISUSPENSOBASEICMS` | — | 'N' | 'N' · PCITEM | só template |
| 137 | `CONSIPISUSPENSOBASEICMS` | — | 'N' | 'N' · PCITEM | só template |
| 138 | `VLALTERCUSTOENT` | — | 0 | 0 · PCITEM | só template |
| 139 | `CONSIDERASTNFCUSTO` | — | 'S' | 'S' · PCITEM | só template |
| 140 | `CONSIDERASTGUIACUSTO` | — | 'S' | 'S' · PCITEM | só template |
| 141 | `CONSIDERASTNFCUSTOCONT` | — | 'S' | 'S' · PCITEM | só template |
| 142 | `CONSIDERASTGUIACUSTOCONT` | — | 'S' | 'S' · PCITEM | só template |
| 143 | `UTILIZABASEPISCOFINSSUSP` | — | 'N' | 'N' · PCITEM | só template |
| 144 | `PERCAFRMM` | — | 0 | 0 · PCITEM | só template |
| 145 | `VLAFRMM` | — | 0 | 0 · PCITEM | só template |
| 146 | `PERCAFRMMCUSTO` | — | 0 | 0 · PCITEM | só template |
| 147 | `VLAFRMMCUSTO` | — | 0 | 0 · PCITEM | só template |
| 148 | `VLPAUTAICMSANTEC` | — | 0 | 0 · PCITEM | só template |
| 149 | `PERCALIQEXTICMANTECIP` | — | 0 | 0 · PCITEM | só template |
| 150 | `PERCALIQINTICMANTECIP` | — | 0 | 0 · PCITEM | só template |
| 151 | `PERCIVAICMANTECIP` | — | 0 | 0 · PCITEM | só template |
| 152 | `VLPISCALCDI` | — | 0 | 0 · PCITEM | só template |
| 153 | `VLCOFINSCALCDI` | — | 0 | 0 · PCITEM | só template |
| 154 | `APLICPERCIVAPAUTAICMSANTECIP` | — | 'N' | 'N' · PCITEM | só template |
| 155 | `VLADICIONALBCICMSANTECIP` | — | 0 | 0 · PCITEM | só template |
| 156 | `PERCICMSFRETEFOBICMSANTECIP` | — | 0 | 0 · PCITEM | só template |
| 157 | `PERCMVAORIGICMSANTECIP` | — | 0 | 0 · PCITEM | só template |
| 158 | `PERCCARGATRIBMEDIAICMSANTECIP` | — | 0 | 0 · PCITEM | só template |
| 159 | `REDBASEIVAICMSANTECIP` | — | 0 | 0 · PCITEM | só template |
| 160 | `REDBASEALIQEXTICMSANTECIP` | — | 0 | 0 · PCITEM | só template |
| 161 | `PERCANTIDUMPING` | — | 0 | 0 · PCITEM | só template |
| 162 | `VLANTIDUMPING` | — | 0 | 0 · PCITEM | só template |
| 163 | `PERCANTIDUMPINGCUSTO` | — | 0 | 0 · PCITEM | só template |
| 164 | `VLANTIDUMPINGCUSTO` | — | 0 | 0 · PCITEM | só template |
| 165 | `NUMPEDMASTERORIGEM` | — | NULL | NULL · PCITEM | só template |
| 166 | `NUMPEDPRINC` | — | NULL | NULL · PCITEM | só template |
| 167 | `NUMSEQORIGEM` | — | NULL | NULL · PCITEM | só template |
| 168 | `VLBASEFCPST` | — | 0 | 0 · PCITEM | só template |
| 169 | `ALIQICMSFECP` | — | 0 | 0 · PCITEM | só template |
| 170 | `VLFECP` | — | 0 | 0 · PCITEM | só template |
| 171 | `VLBASEFCPICMS` | — | 0 | 0 · PCITEM | só template |
| 172 | `PERACRESCIMOFUNCEP` | — | 0 | 0 · PCITEM | só template |
| 173 | `VLACRESCIMOFUNCEP` | — | 0 | 0 · PCITEM | só template |

## PCPEDIDO: 136 colunas

| # | Coluna | 11681 (trace) | Template | Origem (LEIA-ME) | Confere |
|---|---|---|---|---|---|
| 1 | `NUMPED` | 11681.000000 | v_proxnumped | PCCONSUM.PROXNUMPED (FOR UPDATE NOWAIT + 1) · PCPEDIDO | **diferente** |
| 2 | `IDPEDIDOMASTER` | '942/0426' | v_idmaster | PCNUMERADORIMP.PROXNUMPEDIDO (ou o valor digitado) · PCPEDIDO | **diferente** |
| 3 | `CODFILIAL` | '4' | '4' | Texto · C | igual |
| 4 | `CODFORNEC` | 15.000000 | 15 | Numero inteiro · D · CAMPO DE CONTROLE (obrigatorio) | igual |
| 5 | `CODCOMPRADOR` | 201.000000 | 201 | Numero inteiro · E | igual |
| 6 | `CODFUNC` | 349.000000 | 349 | Numero inteiro · F | igual |
| 7 | `FUNCLANC` | 'LUCAS.SILVA' | 'LUCAS.SILVA' | Texto · G | igual |
| 8 | `DTEMISSAO` | 2026.09.02 00:00:00 | TO_DATE('2026-09-02', 'YYYY-MM-DD') | TO_DATE('AAAA-MM-DD','YYYY-MM-DD') · H | igual |
| 9 | `NUMNEGOCIACAO` | 11111.000000 | 11111 | Numero inteiro · I | igual |
| 10 | `VLTOTAL` | 619353.600000 | 619353.6 | Decimal (2 casas) · J | igual |
| 11 | `FRETE` | 'C' | 'C' | Texto · K | igual |
| 12 | `TIPOVENC` | 'P' | 'P' | Texto · L | igual |
| 13 | `TIPOEMBALAGEMPEDIDO` | 'V' | 'V' | Texto · M | igual |
| 14 | `PERCAPRAZO` | 100.000000 | 100 | Decimal (2 casas) · N | igual |
| 15 | `CODMOEDA` | 220.000000 | 220 | Numero inteiro · O | igual |
| 16 | `DTCOTACAO` | 2026.07.19 00:00:00 | TO_DATE('2026-07-19', 'YYYY-MM-DD') | TO_DATE('AAAA-MM-DD','YYYY-MM-DD') · P | igual |
| 17 | `COTACAO` | 5.300000 | 5.3 | Decimal (6 casas) · Q | igual |
| 18 | `INCOTERM` | 'FOB' | 'FOB' | Texto · R | igual |
| 19 | `CODVIA` | 1.000000 | 1 | Numero inteiro · S | igual |
| 20 | `CODFORNECFABRIC` | 15.000000 | 15 | Numero inteiro · T | igual |
| 21 | `CODFORNECPROD` | 15.000000 | 15 | Numero inteiro · U | igual |
| 22 | `CODPAISORIGEM` | 1600.000000 | 1600 | Numero inteiro · V | igual |
| 23 | `CODPAISPROC` | 1600.000000 | 1600 | Numero inteiro · W | igual |
| 24 | `CODPAISAQUISICAO` | 1600.000000 | 1600 | Numero inteiro · X | igual |
| 25 | `NUMINVOCE` | 'TESTECLEI' | 'TESTE' | Texto · Y | **diferente** |
| 26 | `DTEMISSAOINVOCE` | 2026.01.01 00:00:00 | TO_DATE('2026-01-01', 'YYYY-MM-DD') | TO_DATE('AAAA-MM-DD','YYYY-MM-DD') · Z | igual |
| 27 | `DTPREVEMBARQUE` | 2026.02.01 00:00:00 | TO_DATE('2026-02-01', 'YYYY-MM-DD') | TO_DATE('AAAA-MM-DD','YYYY-MM-DD') · AA | igual |
| 28 | `DTPREVCHEGADA` | 2026.03.01 00:00:00 | TO_DATE('2026-03-01', 'YYYY-MM-DD') | TO_DATE('AAAA-MM-DD','YYYY-MM-DD') · AB | igual |
| 29 | `DTPREVENTRADAESTOQUE` | 2026.04.01 00:00:00 | TO_DATE('2026-04-01', 'YYYY-MM-DD') | TO_DATE('AAAA-MM-DD','YYYY-MM-DD') · AC | igual |
| 30 | `CODPORTOCHEGADA` | 1.000000 | 1 | Numero inteiro · AD | igual |
| 31 | `CODPORTONACIONALIZACAO` | 1.000000 | 1 | Numero inteiro · AE | igual |
| 32 | `CODFUNCINCLUSAO` | 349.000000 | 349 | igual a CODFUNC · PCPEDIDO | igual |
| 33 | `CODFUNCALTERACAO` | 349.000000 | 349 | igual a CODFUNC · PCPEDIDO | igual |
| 34 | `CODMOEDACUSTO` | — | 220 | igual a CODMOEDA · PCPEDIDO | só template |
| 35 | `COTACAOCUSTO` | — | 5.3 | igual a COTACAO · PCPEDIDO | só template |
| 36 | `DTCOTACAOCUSTO` | — | TO_DATE('2026-07-19', 'YYYY-MM-DD') | igual a DTCOTACAO · PCPEDIDO | só template |
| 37 | `COTACAOPREVISTA` | — | 5.3 | igual a COTACAO · PCPEDIDO | só template |
| 38 | `CODMOEDAAVISTA` | — | 220 | igual a CODMOEDA · PCPEDIDO | só template |
| 39 | `COTACAOAVISTA` | — | 5.3 | igual a COTACAO · PCPEDIDO | só template |
| 40 | `NUMPROFORMA` | — | 'TESTE' | igual a NUMINVOCE · PCPEDIDO | só template |
| 41 | `DATALANC` | 2026.09.02 00:00:00 | SYSDATE | SYSDATE · PCPEDIDO | **diferente** |
| 42 | `DTPREVENT` | Null | NULL | NULL · PCPEDIDO | igual |
| 43 | `TRANSPORTE` | Null | NULL | NULL · PCPEDIDO | igual |
| 44 | `VLENTREGUE` | Null | NULL | NULL · PCPEDIDO | igual |
| 45 | `OBS` | Null | NULL | NULL · PCPEDIDO | igual |
| 46 | `OBS2` | Null | NULL | NULL · PCPEDIDO | igual |
| 47 | `OBS3` | Null | NULL | NULL · PCPEDIDO | igual |
| 48 | `OBS4` | Null | NULL | NULL · PCPEDIDO | igual |
| 49 | `OBS5` | Null | NULL | NULL · PCPEDIDO | igual |
| 50 | `OBS6` | Null | NULL | NULL · PCPEDIDO | igual |
| 51 | `OBS7` | Null | NULL | NULL · PCPEDIDO | igual |
| 52 | `PRAZO1` | 0.000000 | 0 | 0 · PCPEDIDO | igual |
| 53 | `PRAZO2` | 0.000000 | 0 | 0 · PCPEDIDO | igual |
| 54 | `PRAZO3` | 0.000000 | 0 | 0 · PCPEDIDO | igual |
| 55 | `PRAZO4` | 0.000000 | 0 | 0 · PCPEDIDO | igual |
| 56 | `PRAZO5` | 0.000000 | 0 | 0 · PCPEDIDO | igual |
| 57 | `PRAZO6` | 0.000000 | 0 | 0 · PCPEDIDO | igual |
| 58 | `VLPRODUTO` | Null | NULL | NULL · PCPEDIDO | igual |
| 59 | `CODPLPAG` | Null | NULL | NULL · PCPEDIDO | igual |
| 60 | `DTEMBARQUE` | Null | NULL | NULL · PCPEDIDO | igual |
| 61 | `VLFRETE` | Null | NULL | NULL · PCPEDIDO | igual |
| 62 | `DTLIBERA` | Null | NULL | NULL · PCPEDIDO | igual |
| 63 | `CODPARCELA` | Null | NULL | NULL · PCPEDIDO | igual |
| 64 | `NFIMPORTACAO` | 'S' | 'S' | 'S' · PCPEDIDO | igual |
| 65 | `CALCPISCOFINSBASERED` | 'N' | 'N' | 'N' · PCPEDIDO | igual |
| 66 | `ROTINALANC` | 3010.000000 | 3010 | 3010 · PCPEDIDO | igual |
| 67 | `IMPORTACAO` | 'S' | 'S' | 'S' · PCPEDIDO | igual |
| 68 | `UTILIZAICMSDIFZERADO` | 'N' | 'N' | 'N' · PCPEDIDO | igual |
| 69 | `DTFATUR` | Null | NULL | NULL · PCPEDIDO | igual |
| 70 | `CODFORNECRCA` | Null | NULL | NULL · PCPEDIDO | igual |
| 71 | `CODFORNECIMPORT` | Null | NULL | NULL · PCPEDIDO | igual |
| 72 | `ORCAMENTO` | 'S' | 'S' | 'S' · PCPEDIDO | igual |
| 73 | `PERCADIANTAMENTO` | Null | NULL | NULL · PCPEDIDO | igual |
| 74 | `PERCAVISTA` | Null | NULL | NULL · PCPEDIDO | igual |
| 75 | `DTVENC` | Null | NULL | NULL · PCPEDIDO | igual |
| 76 | `EXPORTADO` | 'N' | 'N' | 'N' · PCPEDIDO | igual |
| 77 | `CODTRANSITARIO` | Null | NULL | NULL · PCPEDIDO | igual |
| 78 | `CODDESPACHANTE` | Null | NULL | NULL · PCPEDIDO | igual |
| 79 | `CODSEGURADORA` | Null | NULL | NULL · PCPEDIDO | igual |
| 80 | `DTCHEGADA` | Null | NULL | NULL · PCPEDIDO | igual |
| 81 | `LOCALEMBARQUE` | Null | NULL | NULL · PCPEDIDO | igual |
| 82 | `DTCOMPROVIMPORT` | Null | NULL | NULL · PCPEDIDO | igual |
| 83 | `DTEMISSAOCONHECEMBARQ` | Null | NULL | NULL · PCPEDIDO | igual |
| 84 | `NUMCONHECEMBARQ` | Null | NULL | NULL · PCPEDIDO | igual |
| 85 | `CANALCONFERENCIA` | 0.000000 | 0 | 0 · PCPEDIDO | igual |
| 86 | `DTEMISSAODOCIMPORT` | Null | NULL | NULL · PCPEDIDO | igual |
| 87 | `NUMDOCIMPORT` | Null | NULL | NULL · PCPEDIDO | igual |
| 88 | `DTPREVNACIONALIZACAO` | Null | NULL | NULL · PCPEDIDO | igual |
| 89 | `CODTERMINALPORTUARIO` | Null | NULL | NULL · PCPEDIDO | igual |
| 90 | `DTEMISSAOPASTA` | Null | NULL | NULL · PCPEDIDO | igual |
| 91 | `NUMPASTA` | Null | NULL | NULL · PCPEDIDO | igual |
| 92 | `IDCONTROLEEMBARQUE` | Null | NULL | NULL · PCPEDIDO | igual |
| 93 | `DTNACIONALIZACAO` | Null | NULL | NULL · PCPEDIDO | igual |
| 94 | `CODFUNCLIBERA` | Null | NULL | NULL · PCPEDIDO | igual |
| 95 | `HORALIBERA` | Null | NULL | NULL · PCPEDIDO | igual |
| 96 | `MINUTOLIBERA` | Null | NULL | NULL · PCPEDIDO | igual |
| 97 | `DTENTRADAESTOQUE` | Null | NULL | NULL · PCPEDIDO | igual |
| 98 | `CODPLPAGADIANT` | Null | NULL | NULL · PCPEDIDO | igual |
| 99 | `CODPLPAGAVISTA` | Null | NULL | NULL · PCPEDIDO | igual |
| 100 | `MEIOTRANSPORTE` | Null | NULL | NULL · PCPEDIDO | igual |
| 101 | `OCORRENCIAS` | Null | NULL | NULL · PCPEDIDO | igual |
| 102 | `CONSMAIORICMSVLPAUTA` | 'N' | 'N' | 'N' · PCPEDIDO | igual |
| 103 | `ISENTOST` | 'X' | 'X' | 'X' · PCPEDIDO | igual |
| 104 | `CODPORTOORIGEM` | Null | NULL | NULL · PCPEDIDO | igual |
| 105 | `CODCLIDEST` | Null | NULL | NULL · PCPEDIDO | igual |
| 106 | `CODFORNECNOTIF` | Null | NULL | NULL · PCPEDIDO | igual |
| 107 | `DOCIMPORTACAO` | Null | NULL | NULL · PCPEDIDO | igual |
| 108 | `MODALIDADEPGTO` | — | NULL | NULL · PCPEDIDO | só template |
| 109 | `CONSIPICALCBASEST` | — | 'N' | 'N' · PCPEDIDO | só template |
| 110 | `UTILIZADESCCALCST` | — | 'N' | 'N' · PCPEDIDO | só template |
| 111 | `CODFORNECFRETE` | — | NULL | NULL · PCPEDIDO | só template |
| 112 | `DTCOTACAOAVISTA` | — | NULL | NULL · PCPEDIDO | só template |
| 113 | `CODDESPACHANTE2` | — | NULL | NULL · PCPEDIDO | só template |
| 114 | `MODALIDADEPGTOADIANT` | — | NULL | NULL · PCPEDIDO | só template |
| 115 | `MODALIDADEPGTOPRAZO` | — | NULL | NULL · PCPEDIDO | só template |
| 116 | `TIPODESCARGA` | — | 'N' | 'N' · PCPEDIDO | só template |
| 117 | `USADRAWBACK` | — | 'N' | 'N' · PCPEDIDO | só template |
| 118 | `DTLI` | — | NULL | NULL · PCPEDIDO | só template |
| 119 | `DTDIFLI` | — | NULL | NULL · PCPEDIDO | só template |
| 120 | `DTREGISTROCANAL` | — | NULL | NULL · PCPEDIDO | só template |
| 121 | `DTZONASECUNDARIA` | — | NULL | NULL · PCPEDIDO | só template |
| 122 | `DTENVIODESPACHANTE` | — | NULL | NULL · PCPEDIDO | só template |
| 123 | `DTVISTORIAORGAOANUENTE` | — | NULL | NULL · PCPEDIDO | só template |
| 124 | `UTILIZAFRETECALCICMS` | — | 'S' | 'S' · PCPEDIDO | só template |
| 125 | `NUMTRANSENTN` | — | NULL | NULL · PCPEDIDO | só template |
| 126 | `CODDOCIMP` | — | NULL | NULL · PCPEDIDO | só template |
| 127 | `CONSCAPATAZIAICMS` | — | 'S' | 'S' · PCPEDIDO | só template |
| 128 | `CODPARCELAORIGEM` | — | NULL | NULL · PCPEDIDO | só template |
| 129 | `TIPOVENCORIGEM` | — | NULL | NULL · PCPEDIDO | só template |
| 130 | `CONSIDERADTVENCRETOR` | — | NULL | NULL · PCPEDIDO | só template |
| 131 | `DTFECHACAMBIO` | — | NULL | NULL · PCPEDIDO | só template |
| 132 | `CONSIDERADTVENCRET` | — | 'N' | 'N' · PCPEDIDO | só template |
| 133 | `DESCREDICMSFCP3010` | — | 'N' | 'N' · PCPEDIDO | só template |
| 134 | `DEDUZIRCAPATAZIABASEII` | — | 'N' | 'N' · PCPEDIDO | só template |
| 135 | `DEDUZIRCAPATAZIABASEPISCOFINS` | — | 'N' | 'N' · PCPEDIDO | só template |
| 136 | `DEDUZIRICMSDIFBASEICMSATECIP` | — | 'S' | 'S' · PCPEDIDO | só template |
