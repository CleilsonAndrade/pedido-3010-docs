# Operação — Roteiro de conferência na MIMO-HOMOLOG

Roteiro que roda o **código da aplicação** contra a homologação e compara com
três referências independentes:
- o que a tela da 3010 gravou no PCITEM;
- a planilha do time (de-para);
- consultas diretas feitas pelo roteiro.

Ele **só lê**, com duas travas:
1. a conexão abre com `SET TRANSACTION READ ONLY`, e qualquer INSERT, UPDATE
   ou DELETE dá erro no próprio Oracle;
2. o roteiro recusa qualquer comando que não comece com SELECT ou WITH,
   inclusive os que vêm do código da aplicação.

No fim, desfaz a transação (ROLLBACK) e fecha a conexão.

---

## 1. Preparar (uma vez)

```
api/.env apontando para a homologação
  DB_HOST=172.20.20.13   ← se for outro, o roteiro para (BASE_CONFIRMADA=S passa por cima)
  DB_SERVICE_NAME, DB_USERNAME, DB_PASSWORD da MIMO-HOMOLOG
  COMEX_API_URL=http://127.0.0.1:8000   (só se for testar a prévia, item 3.6)
```

## 2. Rodar

**Terminal 1**: a API, com o mesmo `.env`:

```bash
cd api
npm install
npm run start:dev          # espera aparecer "Aplicação iniciada | porta 3010"
```

**Terminal 2**: o roteiro. O usuário e a senha são os do WinThor, de alguém
do setor 18. Digite no terminal; **não salve em arquivo**.

Linux ou WSL (a senha é pedida sem aparecer e não fica no histórico do terminal):

```bash
cd api
[ -n "$HOMOLOG_SENHA" ] || { printf 'Senha do WinThor (homologação): '; read -rs HOMOLOG_SENHA; echo; export HOMOLOG_SENHA; }
HOMOLOG_USUARIO=seu.usuario npm run homologacao
```

PowerShell:

```powershell
cd api
$env:HOMOLOG_USUARIO="seu.usuario"
$env:HOMOLOG_SENHA = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR((Read-Host 'Senha do WinThor' -AsSecureString)))
npm run homologacao
```

Leva poucos minutos. No fim aparece o resumo e o nome do arquivo:

```
18 ok · 2 diferente · 0 erro · 7 info · 1 pulado
Relatório: resultado-homologacao-2026-09-24-1015.md
```

**Mande esse `.md` de volta no chat.** Ele não leva senha nem token (o roteiro
tira), mas leva NUMPED, CODPROD, custos e percentuais da homologação.

### Opcional

| Variável | Para quê | Padrão |
|---|---|---|
| `PLANILHA=/caminho/26MZC289F - Final Documents.xls` | item 3.6: a prévia inteira com um LAST de verdade (precisa do comex-api no ar) | pula |
| `API_URL=nao` | só o banco, sem a API | `http://127.0.0.1:3010` |
| `TOKEN=...` | usar um token do Swagger no lugar de usuário e senha | — |
| `FILIAL` `FORNECEDOR` `PAIS` `PORTO` `PRODUTO` `MOEDA` | outro caso para os itens 1.3, 1.9, 2.13 e 3.5 (`PORTO` é o de **nacionalização**) | 4, 15, 1600, 1, 9018, 220 |
| `INVOICE_REPETIDA` | outro caso para o item 2.12 | 26MCS415F |
| `NUMPED_QTSUGESTAO` | item 2.24: pedido lançado manualmente pela 3010 cuja QTSUGESTAO será reconstruída | pula |
| `PEDIDOS_COMPARAR` | quantos pedidos no item 2.14 | 20 |
| `TRANSACAO_SOMENTE_LEITURA=N` | só se aparecer ORA-01456 em algum item (alguma função do WinThor escrevendo); a trava do SELECT continua | S |

---

## 3. O que cada item confere

Situação: **ok** confere · **DIFERENTE** não confere · **ERRO** não rodou
(a mensagem diz por quê) · **info** sem valor esperado, só registro ·
**pulado** faltou algo para rodar.

| # | O que confere | Se der diferente |
|---|---|---|
| 1.1 | Qual base respondeu | Conferir se é mesmo a homologação |
| 1.2 | Fuso do banco e do Node | Só registro |
| 1.3 | Região padrão da filial 4 = 300 | A hipótese do `:NUMREGIAO` da tela cai: "sem preço na região" pode acusar errado |
| 1.4 | Datas da cotação sem hora | A consulta da cotação (dia à meia-noite) pode não achar a cotação |
| 1.5 | TIPOTRIBENTIMP e CON_USATRIBUTACAOPORUF | Só registro: são os valores do caminho que a consulta de impostos copiou |
| 1.6 | País e porto iguais entre si nos pedidos de 2026 | Se houver pedidos, a escolha origem × procedência ou chegada × nacionalização importa: ver a lista |
| 1.7 | Pedido 11681 (o do trace) nesta base | Só registro |
| 1.8 | 11840 e 11841: mesma invoice, fornecedor e negociação | Rever a decisão D. Os valores reais substituem os ilustrativos dos testes |
| 1.9 | CUSTOULTENT do 9018 na filial 4, hoje e por pedido | Evidência para o item 1 dos pontos em aberto (00_STATUS) (o 11723) |
| 1.10 | Cotações com data mais de 7 dias no futuro | Dado errado na base (na 1ª rodada: 30/03/2105). Não é erro da aplicação, mas a tela nunca deve oferecer esse dia |
| 1.11 | Formato do IDPEDIDOMASTER por filial e o PCNUMERADORIMP | Só registro: é o que a gravação (etapa 3) vai ter que gerar |
| 1.12 | Cada CUSTOULTENT gravado para o 9018 procurado nos custos do PCEST de todas as filiais | Só registro: mostra de onde a tela tira o custo (item 1 dos pontos em aberto (00_STATUS)) |
| 1.13 | Próximo número do PCNUMERADORIMP × maior master já usado no ano | A gravação geraria um master que já existe. Na homologação (2ª rodada): 406 × 1047 |
| 1.14 | Pedidos do 9018 que são 2º do master (NUMPEDMASTERORIGEM) e se copiaram o custo do 1º | Só registro: explica custos que não batem com o PCEST da época |
| 2.1 | Banco respondendo | — |
| 2.2 a 2.6 | Listas de moedas, países, portos, fornecedores, compradores e vias | A consulta da tela não bate com esta base |
| 2.7 | Cotação vem do **dia pedido**, não do anterior. Escolhe um dia até hoje cuja véspera tem cotação diferente | A correção do fuso não pegou. Se disser "é a do dia anterior", é o erro antigo |
| 2.8 | Cotação de 19/07/2026 = 5,30 (a do trace) | Só se a base tiver esse dia |
| 2.9 | Maior NUMNEGOCIACAO de 26 | Só registro |
| 2.10 | BH26081/82/83 → 15708/15709/15710 | O de-para não acha o que a planilha do time diz |
| 2.11 | De-para dos 1.941 códigos × planilha do time, separado em CODPROD diferente (com as duas descrições), ambíguo (com os candidatos) e não encontrado | A planilha parou em 06/08: olhar a lista, nem toda diferença é erro |
| 2.12 | Invoice 26MCS415F → 11840 e 11841 (e o tempo) | A consulta da regra D não acha, ou está lenta |
| 2.13 | Impostos do 9018: 20 / 6,5 / 2,1 / 9,65 | A consulta de impostos não reproduz a tela |
| 2.14 | Impostos × PCITEM gravado pela tela nos últimos 20 pedidos, com emissão, quem lançou, histórico do produto e quantos itens cada campo "fora do cálculo" trava. Pedidos sem VLTOTAL (não parecem da tela) ficam fora e listados | Pelo histórico: se o valor mudou para todos a partir de uma data, foi o cadastro; se só um pedido destoa, alguém alterou na tela |
| 2.15 | Campo a campo: consulta de impostos × PCITEM, nos mesmos itens do 2.14 | Só registro: campo que "não bate" em quase todos os itens não é copiado do cadastro pela tela, e não deve travar o item |
| 2.16 | Pedidos com porto de chegada ≠ nacionalização: impostos com cada um × PCITEM | Só registro: diz qual porto a tela usa na tributação (2ª rodada: nacionalização, 6/6) |
| 2.17 | O cálculo da aplicação × os valores que a tela gravou, item a item, só em 1º pedido: base, II, PIS, COFINS, IPI e custo; com frete também VLFRETE, PERCFRETE, despesa aduaneira, outros custos e AFRMM (valores e percentuais, repartidos pelo PESOLIQDI) e o VLTOTAL do pedido | O cálculo não reproduz a tela: ver os itens na lista |
| 2.18 | O frete do pedido repartido entre os itens: por valor, por quantidade ou por cada coluna numérica do PCPRODUT | Só registro: a regra que explicar todos os pedidos é o rateio que o cálculo vai implementar |
| 2.19 | Onde a tela guarda o frete total (o PCPEDIDO.VLFRETE veio vazio): colunas do PCPEDIDO e do PCCONTAINERS (ligado pelo IDCONTROLEEMBARQUE) com a soma; e se o PCITEM.PESOLIQDI é o do cadastro | Só registro: é onde a gravação vai escrever o frete |
| 2.20 | Só nos **1º pedidos** com frete (os 2º têm valores da nota de entrada): o que falta no CUSTOULTPEDCOMPRA (por item) e no VLTOTAL (por pedido). Testa toda coluna do PCITEM e do PCPEDIDO, sozinha e em pares, com e sem cotação; se não bastar, trios entre as colunas de valor. Coluna nula num item vale 0. Mostra também, por pedido, o total de cada despesa (Σ QT × coluna), AFRMM ÷ frete e o que sobra no custo | Só registro: a fórmula achada vira teste do cálculo. Se nenhuma aparecer, o detalhe traz um 1º pedido com frete inteiro |
| 2.21 | Cada pedido comparado: 1º ou 2º do master (NUMPEDMASTERORIGEM), se já teve entrada, se o VLTOTAL é o valor da entrada (VLENTREGUE) e se o II mudou em relação ao 1º | Pedido com frete que é 1º pedido: aí o frete importa para a aplicação, que só cria o 1º |
| 2.22 | VLTOTAL: formas de arredondar (parcela × QT, item × QT, soma no fim, truncado, parcela antes do × QT) com os valores GRAVADOS, em cada 1º pedido | Só registro: a forma que bate em todos é a do cálculo; se for outra, o cálculo muda com teste |
| 2.23 | Como a 3010 gravou em 2026 os campos do cabeçalho que a tela ainda não pede (frete, vencimento, embalagem, % a prazo, datas previstas, fornecedores fabricante e produtor, proforma, países) e o tamanho das colunas OBS | Só registro: decide se a tela ganha o campo ou se a gravação deduz |
| 2.24 | Com `NUMPED_QTSUGESTAO`: exige pedido da rotina 3010; lê QTSUGESTAO, estoque, giro, pendência, prazo de entrega, tempo de reposição, mínimo e múltiplo; infere QTVEZES com/sem pendente e testa o fator comum contra todos os itens | **Info**, até existir rodada real. Se não fechar, conferir primeiro mínimo/múltiplo, prazo usado e se estoque/pendente mudaram. Ver `03_VALIDACOES/ROTEIRO_QTSUGESTAO.md` |
| 3.1 | `/saude` | A API não está no ar ou não vê o banco |
| 3.2 | Login WinThor | Usuário fora do setor 18, senha errada, ou a consulta do login não bate com esta base · se pular, diz qual variável faltou |
| 3.3 | `/cadastros/filiais` com a filial 4 | PCLIB do usuário |
| 3.4 | `/cadastros/cotacao` pelo caminho inteiro | Igual ao 2.7, agora passando pelo DTO |
| 3.5 | `/cadastros/impostos` pelo caminho inteiro | Igual ao 2.13 pela rota |
| 3.6 | `/previa` com um LAST | Só com `PLANILHA=` apontando para um arquivo que existe e o comex-api no ar. Se não der 200, mostra a mensagem da API (ex.: o comex recusou a leitura) |

### Rodada focada da QTSUGESTAO

Depois de lançar um pedido manualmente na 3010 da TESTE:

```bash
cd ~/ww/pedido-3010/api
NUMPED_QTSUGESTAO=<NUMPED> API_URL=nao npm run homologacao
```

O critério de interpretação e as hipóteses que ainda precisam de evidência estão
em `03_VALIDACOES/ROTEIRO_QTSUGESTAO.md`.

---

## 4. Depois

O relatório vira evidência em `03_VALIDACOES/VALIDACAO_HOMOLOGACAO_RODADAS.md` (e o que mudou, no `CHANGELOG.md`). Cada **DIFERENTE** confirmado como
erro vira correção **começando por um teste de regressão que falha**.

Para o ensaio com o lote inteiro de planilhas (prévia de ponta a ponta), use
o que já existe: `PLANILHAS_DIR=... npx jest --config ./test/jest-e2e.json`
(05_OPERACAO/CONFIGURACAO_E_EXECUCAO.md).
