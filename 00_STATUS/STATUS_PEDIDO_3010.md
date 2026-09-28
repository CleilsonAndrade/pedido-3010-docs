# STATUS — pedido-3010

**Status documental:** ATUAL
**Data de referência:** 2026-09-28
**Repositório:** `pedido-3010` (GitHub `CleilsonAndrade/pedido-3010`)
**Branch:** `master`
**HEAD atual:** `8553401 docs: aviso de peso acima de 10%`
**Remoto acompanhado:** `origin/master` em `8553401`
**Estado:** etapa 3 (gravação do 1º pedido) validada na homologação; produção **bloqueada** (`GRAVACAO_3010_ATIVA=N`) até a QTSUGESTAO ser conferida
**Serviços:** `comex-api` (leitura dos LASTs) · Oracle 19c do WinThor (base TESTE na homologação)

---

## 0. Para retomar num chat novo

Primeira mensagem (copiar e colar):

> Estou continuando o projeto pedido-3010. A documentação está no repositório
> `pedido-3010-docs` (anexei). Leia primeiro o `00_STATUS/STATUS_PEDIDO_3010.md`
> e confirme em poucas linhas o que entendeu antes de propor qualquer coisa.
>
> Como eu trabalho: explicações em fluxo passo a passo, com exemplo concreto
> primeiro. Sem termos em inglês que eu não uso; sou prático. Toda correção de
> bug começa por um teste de regressão que falha. Decisão com base em evidência
> (dado real do banco, planilha real), nunca em chute. Comandos git sempre com
> `--no-pager`.
>
> Próximo passo: ver a seção 6 do STATUS.

Anexe, conforme a tarefa:

| Arquivo | Quando precisa |
|---|---|
| `pedido-3010` (zip ou acesso ao GitHub) | sempre |
| `pedido-3010-docs` | sempre |
| `comex_api` (zip) | se for mexer na leitura das planilhas |
| LASTs reais | para testar com dado real (têm senha e preço: não versionar) |
| `Template_-_PEDIDO_MASTER_3010.xlsx` | se for mexer nas colunas da gravação (fora do Git) |
| `TRACE3010_-_PEDIDO_MASTER_2.log` | se for mexer na sequência da gravação |
| traces novos da 3010 | frete e despesas; QTSUGESTAO |

<!-- DOC_VALIDACAO_TIME_2026_09_25:start -->

## Checkpoint 2026-09-25 — primeiro pedido gravado e validação do time

A gravação do 1º pedido (sem frete) rodou de ponta a ponta na homologação:
**NUMPED 11858, master 1049/0426** (`03_VALIDACOES/VALIDACAO_PRIMEIRO_PEDIDO_GRAVADO.md`),
conferido no banco e na própria 3010.

O time da importação gravou 3 LASTs da semana e apontou dois erros e quatro
avisos a tirar; corrigidos nos patches 0048 a 0053
(`03_VALIDACOES/VALIDACAO_TIME_IMPORTACAO_3_LASTS.md`):

```text
peso líquido      PESOLIQDI = N.W. do LAST ÷ quantidade (antes: do cadastro)
item repetido     uma linha só, preço médio ponderado
avisos            lista nova que não bloqueia (total FOB, item repetido, sem peso,
                  peso > 10% do cadastro)
comex             4 avisos dispensados; total FOB vazio não bloqueia
```

Os 3 pedidos do time (11859 a 11861) foram apagados da TESTE; **o reteste com o
código corrigido está pendente**.
<!-- DOC_VALIDACAO_TIME_2026_09_25:end -->

## 1. Estado atual

```text
etapa 1   prévia (só leitura)                      FEITA
etapa 2   tela de conferência, partes 1 a 5        FEITA (impostos editáveis e frete: depois)
etapa 3   gravação do 1º pedido sem frete          FEITA, validada na homologação
etapa 4   produção                                 PENDENTE (QTSUGESTAO; publicação da tela)
```

O que está validado e com que evidência:

```text
cálculo do 1º pedido       71 de 71 itens iguais à homologação; VLTOTAL a até 2 centavos
backend contra a TESTE     17ª rodada: 21 ok (login, cadastros, cotação, impostos, prévia)
gravação                   11858 conferido no banco e na 3010 (valores até a 6ª casa)
peso e item repetido       regras novas cobertas por teste; reteste do time pendente
```

## 2. Patches

Aplicados em ordem com `git am` sobre o pacote original; todos no GitHub
(`origin/master` em `8553401` até o 0053; o 0054 é aplicado junto com a criação deste repositório).

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

Fora da sequência: `comex-api-rota-leitura.patch` e
`comex-api-senha-fora-do-teste.patch`, aplicados no comex-api
(`04_CONTRATOS/CONTRATO_COMEX_API.md`).

## 3. Gate atual (25/09)

```text
API    unidade          318 / 318 PASS
API    ponta a ponta    48 PASS, 2 pulados (dependem do comex no ar)
tela   Vitest           69 / 69 PASS
tsc, eslint, build      PASS (API e tela)
regra do teste de regressão   PASS (todos os fix com teste)
cópia limpa             os 53 patches aplicam sobre o pacote original
```

## 4. Base TESTE (homologação)

```text
serviço                  TESTE em 172.20.20.13 (não CDBTST)
PCNUMERADORIMP 2026      1050 (acertado em 25/09; estava em 406 com 1048 em uso)
PCCONSUM                 não devolvido
pedidos da aplicação     11858 (fica, referência); 11859 a 11861 apagados
pedidos sem item         10483 a 10490 (testes do template) apagados antes
gatilhos do PCITEM       os 3 ENABLED
```

Roteiros: `05_OPERACAO/BASE_TESTE.md`.

## 5. Em aberto

```text
QTSUGESTAO        decidido calcular como a 3010; a conta não aparece no trace. Conferir
                  lançando um pedido PELA 3010 na TESTE, com um item do roteiro lendo
                  estoque e giro na mesma hora. É o que libera a produção.
2º pedido         qual ação da 3010 o gera e por que o VLTOTAL muda (não bloqueia)
frete e despesas  onde a 3010 guarda os totais, em que moeda se digita o frete, se o
                  AFRMM é digitado: precisa do trace de um lançamento com despesas
custo em dólar    a 3010 soma o frete em USD sem converter no CUSTOULTPEDCOMPRA;
                  replicado; AVISAR O TIME
comex             levar a regra código × descrição para o comex (hoje só no pedido-3010)
tela              impostos editáveis; frete e despesas; publicação (servidor que entrega
                  o dist e repassa /api)
API               CORS só para o endereço da tela (hoje aceita qualquer origem)
desfazer          rota prevista (só sem entrada), não implementada
backups do .40    teste de restauração pendente; MSSRV005 no Ubuntu 18.04
```

## 6. Próximos passos, em ordem

```text
1. reteste do time com os 3 LASTs (26MIW185F, 26MOC267F, 26MSR296F) no ambiente novo
   de teste; conferir PJ10PCM numa linha e os pesos do LAST (VALIDACAO_TIME, seção 7)
2. QTSUGESTAO: preparar o item do roteiro; lançar um pedido pela 3010 na TESTE; achar
   a conta
3. impostos editáveis na tela
4. frete e despesas (depois do trace)
5. publicação da tela
6. produção: GRAVACAO_3010_ATIVA=S por decisão, primeiro para um usuário
```

## 7. Como trabalhar neste projeto

```text
correção de bug       começa por um teste de regressão que falha (gancho + CI)
evidência             dado real do banco, trace ou LAST real; hipótese é dita como hipótese
toda gravação         precisa de caminho de volta
explicação            fluxo passo a passo, exemplo concreto primeiro, sem termos em inglês
git                   comandos com saída sempre com --no-pager
patches               aplicar só na máquina em uso e fazer push; na outra, pull --rebase
entrega               todo commit de código vira patch; conferir "commits = patches" e
                      aplicar os patches numa cópia limpa antes de entregar
```
