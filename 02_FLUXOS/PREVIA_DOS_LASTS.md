# Fluxo — Prévia dos LASTs

Endpoint:

```text
POST /api/v1/previa        multipart, campo "arquivos" (até 60 LASTs, .xls/.xlsx)
```

A prévia **não grava nada** e não guarda estado: não existe número de prévia.
Ela mostra cada pedido como vai para a 3010 e o que impede gravar.

## 1. Sequência

```text
LASTs enviados pela tela
      |
      v
comex-api  POST /api/v1/import-documents/leitura
      |    lê o .xls com senha, corrige peso invertido, embute encargo e
      |    arredonda o preço como na invoice (o mesmo processamento da invoice)
      v
um processo por LAST (1 planilha = 1 pedido)
      |
      |-- SHA-256 de cada arquivo (a gravação confere que é o mesmo)
      |-- ocorrências do comex, menos as dispensadas pelo time
      |-- de-para código de fábrica -> CODPROD (uma ida ao banco por lote)
      |-- regra código × descrição
      |-- pedidos da 3010 com a mesma invoice (decisão D)
      |-- peso do cadastro dos produtos achados (aviso de peso)
      v
PedidoPreviaDto por LAST: itens, pendências, avisos, podeGravar
```

## 2. De-para (código de fábrica -> CODPROD)

```text
1. PCPRODUT.CODFAB igual (sem espaço nas pontas, maiúsculo)
2. CODFAB sem hífen, # e espaço
sempre com DTEXCLUSAO IS NULL (produto excluído não entra em pedido de compra)

0 candidatos     -> PRODUTO_NAO_ENCONTRADO
1 candidato      -> resolvido
2+ candidatos    -> PRODUTO_AMBIGUO (a tela mostra os candidatos para escolher)
```

## 3. Pendências (bloqueiam: `podeGravar = false`)

```text
LEITURA_FALHOU               o comex não conseguiu ler a planilha
BLOQUEIO_COMEX               ocorrência de nível "bloqueio" do comex (fora as dispensadas
                             e o total FOB vazio)
CODIGO_DESCRICAO_DIVERGENTE  o código da linha e o começo da descrição apontam produtos
                             diferentes (ex.: BH26081 com descrição "BH26082 ..."):
                             a tela mostra os dois lados para escolher
PRODUTO_AMBIGUO              o código acha mais de um produto
PRODUTO_NAO_ENCONTRADO       nenhum produto com esse código: resolve no cadastro do WinThor
```

O que se resolve onde (decisão de 24/09): linha trocada e ambíguo, **na tela**;
produto não encontrado, sem tributação ou sem peso, **no cadastro do WinThor**
(e depois solta o mesmo LAST de novo); leitura que falhou e bloqueio do comex,
**no arquivo**. O LAST não deve ser editado à mão: é documento do fornecedor, e
o comex emite invoice e packing a partir dele.

## 4. Avisos (não bloqueiam)

```text
TOTAL_FOB_CALCULADO         o LAST não traz a soma dos valores: a tela somou os itens
ITEM_REPETIDO               o mesmo produto em mais de uma linha: vai somado numa linha
                            só (preço médio ponderado quando os preços diferem)
SEM_PESO_NO_LAST            linha sem N.W.: vai o peso do cadastro
PESO_DIFERENTE_DO_CADASTRO  peso do LAST difere mais de 10% do cadastro (para cima ou
                            para baixo); só em linha com produto definido e cadastro
                            com peso
```

A regra dos itens repetidos é **a mesma** na prévia (para avisar) e na gravação
(para somar): `api/src/modules/previa/regras/itens-repetidos.regra.ts`.

## 5. Ocorrências do comex

Passam para a tela em `ocorrenciasComex`, **menos** as que o time dispensou
(25/09): `cabecalho.vazio` com `cntr_number` (contêiner), `port_loading` (porto de
embarque) e `to` (cliente), e `conta.ausente` (imagem dos dados bancários). O
total FOB vazio (`cabecalho.vazio` / `total_fob_price`) aparece, mas não vira
pendência. Contrato em `04_CONTRATOS/CONTRATO_COMEX_API.md`.

## 6. Invoice já lançada (decisão D)

A prévia devolve `pedidosComMesmaInvoice`: os pedidos da 3010 com a mesma
invoice, comparada em maiúscula e **sem espaço em branco nas pontas**
(`REGEXP_REPLACE`, porque há NUMINVOCE gravado com tabulação; o `TRIM` do Oracle
não tira tabulação). Pedidos cancelados **entram** na comparação.

**Invoice repetida é master repetido, não pedido repetido:** o 2º pedido do
master (criado pela própria 3010 na nacionalização) não conta como outro
lançamento. No mesmo master, o menor NUMPED é o 1º; o `NUMPEDPRINC` nem sempre
vem preenchido e serve só de confirmação.

## 7. O que a prévia devolve (resumo)

```text
arquivo, sha256, podeGravar, gravacaoAtiva
cabecalho        invoice, data, fornecedor na planilha, portos, contêiner, totais
itens            linha, código, descrição, quantidade, preço, total, peso (N.W.),
                 de-para, divergência
pendencias       o que bloqueia
avisos           o que não bloqueia
ocorrenciasComex
pedidosComMesmaInvoice
camposParaPreencher   o que a tela precisa coletar (filial, fornecedor, comprador...)
```
