# STATUS — pedido-3010

**Status documental:** EM MIGRAÇÃO para o modelo documental com ESP
**Data de referência:** 2026-10-07
**Repositório:** `pedido-3010` (GitHub `CleilsonAndrade/pedido-3010`)
**Branch:** `master`
**HEAD acompanhado:** `51346d6 test: restaura gate da API após cotação BCB`
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

## 1. Estado atual

- Primeiro pedido homologado na base TESTE: `NUMPED 11858`, master `1049/0426`.
- `QTSUGESTAO` homologada para `CONSIDERAESTPENDSUGCOMPRA=N`, com o pedido nativo `11866` reproduzindo 2/2 itens.
- O ramo `CONSIDERAESTPENDSUGCOMPRA=S` continua não homologado e bloqueado pela aplicação.
- As evoluções funcionais posteriores a `b813ceb` chegaram até `a5362cd`, com BCB/PTAX + 5%, defaults de filial/comprador, proteção concorrente da cotação e validação da cronologia das datas. O commit `51346d6` restaurou e validou o gate técnico da API após essas mudanças.
- Essas evoluções posteriores estão implementadas e cobertas por testes automatizados, mas ainda aguardam homologação funcional.
- O pedido `11869` evidenciou a cronologia inválida antes de `a5362cd`; ele não representa homologação pós-correção.
- Produção continua não publicada.

## 2. Histórico de implementação

A evolução detalhada dos patches `0001` a `0055` e o fechamento da `QTSUGESTAO` foram arquivados em `99_HISTORICO/ARQUIVADOS/HISTORICO_PATCHES_0001_0055.md`.

A cronologia das mudanças permanece registrada também em `CHANGELOG.md`.

## 3. Gate técnico atual — 06/10/2026

Código validado: `pedido-3010 @ 51346d6`.

```text
API    lint             PASS
API    unidade          349 / 349 PASS
API    ponta a ponta    48 PASS, 2 pulados
API    build            PASS
API    diff --check     PASS
tela   Vitest           76 / 76 PASS
tela   build            PASS
```

Os 2 testes E2E pulados dependem do `comex-api` real e/ou das planilhas externas de homologação.

O gate anterior de 25/09 foi preservado em `99_HISTORICO/ARQUIVADOS/GATE_2026-09-25.md`.

## 4. Base TESTE — evidências de homologação

A base TESTE foi usada nas homologações documentadas do projeto.

- `11858` (`1049/0426`): primeiro pedido gravado e homologado como referência.
- `11866`: pedido nativo usado para homologar a `QTSUGESTAO` no ramo `CONSIDERAESTPENDSUGCOMPRA=N`; 2/2 itens reproduzidos pela aplicação.
- `11869`: evidência da cronologia inválida permitida antes de `a5362cd`; não representa homologação pós-correção.
- O ramo `CONSIDERAESTPENDSUGCOMPRA=S` continua não homologado e bloqueado pela aplicação.
- Antes de nova homologação, conferir novamente `PCCONSUM`, `PCNUMERADORIMP` e os maiores números já usados; os valores registrados em 25/09 são históricos.

O procedimento operacional e o snapshot de 25/09 permanecem em `06_OPERACAO/BASE_TESTE.md`.

## 5. Em aberto

- **Homologação pós-`b813ceb`:** BCB/PTAX + 5%, defaults de filial/comprador, proteção concorrente da cotação e validação da cronologia estão implementados e com gate técnico verde, mas ainda aguardam homologação funcional.
- **Cronologia:** executar homologação pós-`a5362cd`; o pedido `11869` prova apenas o comportamento incorreto anterior à correção.
- **QTSUGESTAO/S:** filial com `CONSIDERAESTPENDSUGCOMPRA=S` continua não homologada e bloqueada até existir evidência da 3010.
- **2º pedido:** identificar qual ação da 3010 o gera e por que o `VLTOTAL` muda; não bloqueia o primeiro pedido.
- **Frete e despesas:** confirmar no trace onde a 3010 persiste os totais, moeda usada no frete e tratamento do AFRMM.
- **Custo em dólar:** a reprodução atual soma frete em USD sem conversão no `CUSTOULTPEDCOMPRA`, conforme comportamento observado; manter o alerta ao time até validação funcional.
- **COMEX:** avaliar mover para o `comex-api` a regra de código × descrição que hoje também é tratada no `pedido-3010`.
- **Tela:** impostos editáveis, frete/despesas e publicação ainda não concluídos.
- **API:** restringir CORS quando o endereço definitivo da tela estiver definido.
- **Desfazer:** fluxo previsto para pedido sem entrada, ainda não implementado.
- **Produção:** não publicada; `GRAVACAO_3010_ATIVA` deve permanecer controlada até decisão explícita de ativação.

## 6. Próximos passos, em ordem

1. **Homologar as evoluções posteriores a `b813ceb` na TESTE:** BCB/PTAX + 5%, defaults de filial/comprador, proteção da cotação e cronologia das datas; registrar evidências sem reutilizar o `11869` como homologação pós-correção.
2. **Retestar o fluxo já homologado com os LASTs do time** (`26MIW185F`, `26MOC267F`, `26MSR296F`), incluindo pesos do LAST e conferências já previstas no roteiro de validação.
3. **Obter trace de frete e despesas** para fechar persistência, moeda do frete e AFRMM antes de evoluir esse trecho.
4. **Evoluir a tela** com impostos editáveis e frete/despesas somente depois das regras correspondentes estarem validadas.
5. **Preparar publicação da tela e restringir CORS** para o endereço definitivo da aplicação.
6. **Planejar ativação em produção** somente após homologação funcional, mantendo `GRAVACAO_3010_ATIVA` controlada e iniciando com escopo restrito.
7. **Homologar `CONSIDERAESTPENDSUGCOMPRA=S` apenas quando houver caso real/evidência da 3010**; até lá, manter o bloqueio atual.
