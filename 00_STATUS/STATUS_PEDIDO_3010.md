# STATUS — pedido-3010

**Status documental:** EM MIGRAÇÃO para o modelo documental com ESP
**Data de referência:** 2026-10-06
**Repositório:** `pedido-3010` (GitHub `CleilsonAndrade/pedido-3010`)
**Branch:** `master`
**HEAD acompanhado:** `51346d6 fix: valida cronologia das datas previstas`
**Remoto acompanhado:** `origin/master` em `51346d6`
**Baseline funcional homologado:** `b813ceb feat: calcula QTSUGESTAO como a rotina 3010`
**Estado:** primeiro pedido homologado na TESTE e `QTSUGESTAO` homologada no ramo `CONSIDERAESTPENDSUGCOMPRA=N`; evoluções posteriores até `51346d6` implementadas e testadas, mas ainda sem homologação funcional; produção não publicada e protegida por `GRAVACAO_3010_ATIVA`
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
**NUMPED 11858, master 1049/0426** (`04_VALIDACOES/VALIDACAO_PRIMEIRO_PEDIDO_GRAVADO.md`),
conferido no banco e na própria 3010.

O time da importação gravou 3 LASTs da semana e apontou dois erros e quatro
avisos a tirar; corrigidos nos patches 0048 a 0053
(`04_VALIDACOES/VALIDACAO_TIME_IMPORTACAO_3_LASTS.md`):

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

- Primeiro pedido homologado na base TESTE: `NUMPED 11858`, master `1049/0426`.
- `QTSUGESTAO` homologada para `CONSIDERAESTPENDSUGCOMPRA=N`, com o pedido nativo `11866` reproduzindo 2/2 itens.
- O ramo `CONSIDERAESTPENDSUGCOMPRA=S` continua não homologado e bloqueado pela aplicação.
- O código atual avançou de `b813ceb` até `51346d6` com BCB/PTAX + 5%, defaults de filial/comprador, proteção concorrente da cotação e validação da cronologia das datas.
- Essas evoluções posteriores estão implementadas e cobertas por testes automatizados, mas ainda aguardam homologação funcional.
- O pedido `11869` evidenciou a cronologia inválida antes de `51346d6`; ele não representa homologação pós-correção.
- Produção continua não publicada.

## 2. Histórico de implementação

A evolução detalhada dos patches `0001` a `0055` e o fechamento da `QTSUGESTAO` foram arquivados em `99_HISTORICO/ARQUIVADOS/HISTORICO_PATCHES_0001_0055.md`.

A cronologia das mudanças permanece registrada também em `CHANGELOG.md`.

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

Roteiros: `06_OPERACAO/BASE_TESTE.md`.

## 5. Em aberto

```text
QTSUGESTAO/S      filial com CONSIDERAESTPENDSUGCOMPRA='S' ainda não homologada;
                  a API recusa esse ramo até existir evidência da 3010.
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
2. impostos editáveis na tela
3. frete e despesas (depois do trace)
4. publicação da tela
5. produção: GRAVACAO_3010_ATIVA=S por decisão, primeiro para um usuário
6. se aparecer filial com CONSIDERAESTPENDSUGCOMPRA='S', homologar esse ramo
   antes de permitir gravação nela
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
