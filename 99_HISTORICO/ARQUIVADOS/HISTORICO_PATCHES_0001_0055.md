# Histórico de patches e fechamento da QTSUGESTAO

## 2. Patches

Aplicados em ordem com `git am` sobre o pacote original. O histórico abaixo
mantém a sequência 0001 a 0055. O patch **0055 foi aplicado** e abriu a
investigação da `QTSUGESTAO`; o fechamento posterior entrou nos commits
`c96e389` e `b813ceb`. O remoto atual está em `origin/master = b813ceb`.

### Etapa 1 e homologação: regras, prévia, impostos e o roteiro (23/09)

```text
0001  fix: cotação consultava o dia anterior (data ia para o Oracle como Date)
0002  feat: rota que confere o NUMNEGOCIACAO (regra A) para a tela
0003  feat: regra A avisa NUMNEGOCIACAO fora de 5 dígitos (602, 266022)
0004  feat: prévia mostra os pedidos do WinThor com a mesma invoice (decisão D)
0005  feat: rota dos impostos do cadastro por item (consulta da tela da 3010)
0006  feat: roteiro de conferência na homologação (npm run homologacao)
0007  fix: IDPEDIDOMASTER é texto (1046/0426), não número
0008  feat: roteiro ampliado com a evidência dos DIFERENTES da 1ª rodada
0009  fix: PERCDESCICMSDIF não trava o item (a tela não copia esse campo)
0010  fix: tributação usa o porto de NACIONALIZAÇÃO, não o de chegada
0011  feat: 3ª rodada do roteiro (cálculo item a item, frete, numerador, ambíguos)
0012  fix: roteiro não cai com coluna LOB no SELECT * do PCPRODUT (item 2.11)
0013  style: conversão de tipo desnecessária no texto() do roteiro
```

### Cálculo do 1º pedido: frete, despesas, AFRMM e VLTOTAL (23 e 24/09)

```text
0014  feat: frete no cálculo (rateio pelo PESOLIQDI e base com o frete por unidade)
0015  feat: 4ª rodada do roteiro (pedido inteiro com frete, onde fica o frete total)
0016  fix: roteiro conta todos os itens do 2.17, liga o PCCONTAINERS pelo embarque e diz qual variável faltou
0017  feat: 5ª rodada do roteiro busca a fórmula do custo e do VLTOTAL com frete (2.20)
0018  feat: roteiro 2.21, pedido com frete é o 2º pedido do master?
0019  fix: roteiro busca a fórmula do frete só em 1º pedido e avisa PLANILHA que não existe
0020  fix: busca do 2.20 não descarta coluna nula em alguns itens; resumo de despesas por pedido
0021  feat: despesas do pedido no cálculo (aduaneira, outros custos, AFRMM, custo e VLTOTAL da 3010)
0022  feat: 9ª rodada do roteiro confere despesas pelo cálculo novo; 3.6 mostra a mensagem da API
0023  fix: AFRMM é total informado (10% do frete sem centavos) e o roteiro estima os totais pelo que reproduz os itens
0024  fix: roteiro estima o frete em dólar ou em reais; 2.22 testa o arredondamento do VLTOTAL com os valores gravados
0025  fix: estimativa do frete usa o PERCFRETE e faixa proporcional; VLTOTAL com valores internos no 2.17
0026  feat: tolerância de 2 centavos no VLTOTAL do 1º pedido (decisão de 24/09)
0027  feat: rota de cálculo do pedido para a tela (POST /calculo/pedido, sem gravar)
0028  fix: roteiro 3.6 mostra a mensagem das pendências da prévia
```

### Etapa 2: a tela, partes 1 a 4 (24 e 25/09)

```text
0029  feat: tela, parte 1 (Angular em web/): entrar, conferir LASTs e ver cada pedido
0030  feat: tela, parte 2: escolher o produto na linha trocada e no ambíguo
0031  fix: tela diz quando o comex recusou a leitura, não que ele não respondeu
0032  fix: resumo da conferência acompanha as escolhas e fala certo de um pedido só
0033  feat: pedido já lançado agrupado por master, com o 1º e o 2º pedido
0034  fix: 1º e 2º pedido do master pela regra do master, não pelo NUMPEDPRINC
0035  feat: tela, parte 3: os dados do pedido na 3010 (fornecedor, filial, cotação, portos)
0036  fix: pendência de cotação mostra a moeda como está no cadastro
0037  feat: tela, parte 4: negociação sugerida e conferida pela regra A enquanto digita
```

### Etapa 3: o cabeçalho, a montagem, a execução, a rota e a tela da gravação (25/09)

```text
0038  feat: roteiro 2.23, campos do cabeçalho que a tela ainda não pede
0039  feat: roteiro 2.23 separa o 1º do 2º pedido e mostra as OBS e as proformas diferentes
0040  fix: checagem de invoice repetida não deixa escapar invoice gravada com tabulação
0041  feat: montagem da gravação do 1º pedido (PCPEDIDO e PCITEM como a 3010 grava)
0042  feat: execução da gravação do 1º pedido numa transação só (ainda sem rota)
0043  feat: rota POST /gravacao, com o servidor conferindo tudo antes de gravar
0044  fix: peso líquido da DI como a 3010 (PESOLIQ quando falta o PESOLIQDI)
0045  feat: prévia devolve o SHA-256 de cada arquivo
0046  feat: tela, parte 5: gravar na 3010 (datas previstas, proforma, confirmação e resultado)
0047  fix: numerador travado por outra sessão vira recusa clara, não "Internal server error"
```

### Validação do time da importação com 3 LASTs (25/09)

```text
0048  feat: prévia avisa o que não bloqueia (total FOB calculado, item repetido, linha sem peso)
0049  fix: gravação soma o item repetido e grava o peso líquido do LAST
0050  feat: tela mostra os avisos da prévia (não impedem gravar)
0051  fix: aviso do total FOB quando falta a soma do LAST, mesmo com total na invoice
0052  feat: prévia dispensa os avisos do comex que o time não usa; total FOB vazio não bloqueia
0053  feat: aviso quando o peso do LAST difere mais de 10% do cadastro
```

### Documentação (28/09)

```text
0054  docs: documentação movida para o repositório pedido-3010-docs
      (+ git rm dos 4 documentos antigos de docs/, fora do patch)
```

### Fechamento da QTSUGESTAO (28 a 30/09)

O patch 0055 abriu a investigação em modo somente leitura. A hipótese inicial
incluía `QTVEZES`, mas ela caiu após testes manuais na própria
**PCSIS3010 v37.0.08.071**.

Pedido nativo de referência:

```text
NUMPED              11866
CODFILIAL           4
CODFORNEC           15
ROTINALANC          3010
CONSIDERAESTPENDSUGCOMPRA = N
```

Conta homologada para esse caminho:

```text
ESTOQUE_IDEAL =
    QTGIRODIA × (PRAZOENTREGA + TEMREPOS)

QTSUGESTAO =
    ESTOQUE_IDEAL - ESTOQUE_DISPONIVEL
```

Fontes usadas pela implementação:

```text
QTGIRODIA            PCEST.QTGIRODIA
PRAZOENTREGA         PCFORNEC.PRAZOENTREGA
TEMREPOS             PCPRODUT.TEMREPOS
ESTOQUE_DISPONIVEL   PKG_ESTOQUE.ESTOQUE_DISPONIVEL(CODPROD, CODFILIAL, 'C')
```

Casos reais do pedido 11866:

```text
8360   1 × (150 + 21) - 925 = -754
11190  10 × (150 + 21) - 0 = 1710
```

O roteiro 2.24 reproduziu **2 de 2 itens**, com diferença zero.

Conclusões do caminho homologado:

```text
QTVEZES                         não entra na conta-base observada
QTSUGESTAO negativa             é preservada
QTMINSUGCOMPRA/MULTIPLOCOMPRAS  sem caso positivo observado na filial 4
pendência de compra             filial 4 não considera
```

A base TESTE não possui filial com
`CONSIDERAESTPENDSUGCOMPRA='S'`. Esse ramo continua **não homologado**; a API
recusa a gravação nesse cenário em vez de assumir uma fórmula.

Código final:

```text
c96e389  fix: usa PCEST na validacao da QTSUGESTAO
b813ceb  feat: calcula QTSUGESTAO como a rotina 3010
```

Validação final do `b813ceb`, em transação somente leitura:

```text
16 ok · 5 diferente · 0 erro · 17 info · 2 pulado

2.24
pedido 11866 · 2 item(ns) · pendente não considerado ·
conta-base reproduz 2/2
```

Fora da sequência: `comex-api-rota-leitura.patch` e
`comex-api-senha-fora-do-teste.patch`, aplicados no comex-api
(`05_CONTRATOS/CONTRATO_COMEX_API.md`).

