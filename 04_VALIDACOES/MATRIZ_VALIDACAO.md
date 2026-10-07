# Matriz de validação — Pedido Master 3010

**Natureza:** índice de rastreabilidade entre os critérios de aceite da ESP e o estado de validação conhecido.

Esta matriz referencia os `CN` da `03_ESPECIFICACOES/ESP_PEDIDO_MASTER.md`.
Ela não redefine nem duplica os cenários descritos na ESP.

Os **85 critérios de aceite da ESP estão reconciliados nesta matriz** com a evidência atualmente conhecida.
A classificação registra o nível dessa evidência e não significa que todos os cenários estejam funcionalmente homologados.

## Estados usados

A matriz distingue o nível da evidência. Os qualificadores de cada linha devem
ser lidos junto com o escopo informado na coluna de referência.

- **HOMOLOGADO:** existe evidência funcional documentada no escopo indicado.
- **IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS:** o comportamento possui
  cobertura automatizada, mas isso não equivale, por si só, a homologação funcional.
- **HOMOLOGAÇÃO A VALIDAR:** comportamento implementado e testado que ainda precisa
  de validação funcional no ambiente de homologação.
- **RETESTE FUNCIONAL A VALIDAR:** regra corrigida após evidência do time e já
  coberta por testes, mas cujo reteste com o fluxo real permanece pendente.
- **IMPLEMENTADO POR INSPEÇÃO DO CÓDIGO · TESTE/HOMOLOGAÇÃO ESPECÍFICOS A VALIDAR:**
  o comportamento está presente no código, mas ainda não possui teste ou evidência
  funcional específica que prove o cenário isoladamente.

## Matriz

| CN | Estado | Referência atual |
|---|---|---|
| `P3010-HU1-RN1-CN1` | HOMOLOGADO NA TESTE | VALIDACAO_HOMOLOGACAO_RODADAS.md — login WinThor setor 18 com token |
| `P3010-HU1-RN1-CN2` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | auth.service.spec.ts + winthor-credential-auth.provider.spec.ts — credencial inválida retorna 401 |
| `P3010-HU1-RN2-CN1` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | winthor-credential-auth.provider.spec.ts — setor não autorizado retorna 403 |
| `P3010-HU1-RN3-CN1` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | gravacao.service.spec.ts — filial fora da PCLIB é recusada |
| `P3010-HU2-RN1-CN1` | HOMOLOGADO NA TESTE | VALIDACAO_HOMOLOGACAO_RODADAS.md — etapa 1 e prévia real somente leitura |
| `P3010-HU2-RN2-CN1` | HOMOLOGADO COM LASTS REAIS | VALIDACAO_HOMOLOGACAO_RODADAS.md — ensaio com 33 planilhas reais |
| `P3010-HU2-RN3-CN1` | HOMOLOGADO COM LAST REAL | VALIDACAO_HOMOLOGACAO_RODADAS.md — 26MZC289F via comex-api |
| `P3010-HU2-RN3-CN2` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | previa.service.spec.ts — falha de leitura gera LEITURA_FALHOU sem derrubar o lote |
| `P3010-HU2-RN4-CN1` | HOMOLOGADO COM LAST REAL | previa.e2e-spec.ts + VALIDACAO_HOMOLOGACAO_RODADAS.md — produto resolvido |
| `P3010-HU2-RN4-CN2` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | previa.service.spec.ts — produto sem candidato gera PRODUTO_NAO_ENCONTRADO |
| `P3010-HU2-RN4-CN3` | HOMOLOGADO COM LASTS REAIS | VALIDACAO_HOMOLOGACAO_RODADAS.md — família HTC ambígua vira pendência |
| `P3010-HU2-RN5-CN1` | HOMOLOGADO COM LASTS REAIS | EVIDENCIAS_TRACE_E_BANCO.md + previa.e2e-spec.ts — código × descrição divergentes |
| `P3010-HU2-RN6-CN1` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS · RETESTE FUNCIONAL A VALIDAR | itens-repetidos.regra.spec.ts — mesmo preço |
| `P3010-HU2-RN6-CN2` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS · RETESTE FUNCIONAL A VALIDAR | itens-repetidos.regra.spec.ts + VALIDACAO_TIME_IMPORTACAO_3_LASTS.md |
| `P3010-HU2-RN7-CN1` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS · RETESTE FUNCIONAL A VALIDAR | gravacao.service.spec.ts + itens-repetidos.regra.spec.ts |
| `P3010-HU2-RN7-CN2` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS · RETESTE FUNCIONAL A VALIDAR | gravacao.service.spec.ts + previa.service.spec.ts |
| `P3010-HU2-RN7-CN3` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS · RETESTE FUNCIONAL A VALIDAR | previa.service.spec.ts — limite de 10% para peso |
| `P3010-HU2-RN8-CN1` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | previa.service.spec.ts — bloqueio relevante vira pendência |
| `P3010-HU2-RN8-CN2` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS · RETESTE FUNCIONAL A VALIDAR | previa.service.spec.ts + VALIDACAO_TIME_IMPORTACAO_3_LASTS.md |
| `P3010-HU2-RN8-CN3` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS · RETESTE FUNCIONAL A VALIDAR | previa.service.spec.ts + VALIDACAO_TIME_IMPORTACAO_3_LASTS.md |
| `P3010-HU2-RN9-CN1` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | previa.service.spec.ts — invoice inexistente retorna lista vazia |
| `P3010-HU2-RN9-CN2` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | gravacao.service.spec.ts — invoice existente exige motivo |
| `P3010-HU2-RN9-CN3` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | pedidos-da-invoice.oracle.spec.ts — 2º pedido usa NUMPEDPRINC do 1º pedido do mesmo master |
| `P3010-HU2-RN9-CN4` | IMPLEMENTADO POR INSPEÇÃO DO CÓDIGO · TESTE/HOMOLOGAÇÃO ESPECÍFICOS A VALIDAR | pedidos-da-invoice.oracle.ts — consulta por NUMINVOCE não exclui POSICAO/DTCANCEL ou outro estado de cancelamento |
| `P3010-HU3-RN1-CN1` | IMPLEMENTADO · VALIDADO POR TESTES · HOMOLOGAÇÃO A VALIDAR | ESP + gate técnico atual |
| `P3010-HU3-RN1-CN2` | IMPLEMENTADO · VALIDADO POR TESTES · HOMOLOGAÇÃO A VALIDAR | ESP + gate técnico atual |
| `P3010-HU3-RN1-CN3` | IMPLEMENTADO · VALIDADO POR TESTES · HOMOLOGAÇÃO A VALIDAR | ESP + gate técnico atual |
| `P3010-HU3-RN1-CN4` | IMPLEMENTADO · VALIDADO POR TESTES · HOMOLOGAÇÃO A VALIDAR | ESP + gate técnico atual |
| `P3010-HU3-RN2-CN1` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | dados-pedido.spec.ts — fornecedor compatível pode ser selecionado na tela |
| `P3010-HU3-RN2-CN2` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | gravacao.service.spec.ts — fornecedor bloqueado no WinThor impede a gravação |
| `P3010-HU3-RN3-CN1` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | dados-pedido.spec.ts — fornecedor selecionado define o país de origem |
| `P3010-HU3-RN4-CN1` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | dados-pedido.spec.ts — destino do LAST inicia o porto de chegada correspondente |
| `P3010-HU3-RN5-CN1` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | dados-pedido.spec.ts — nacionalização acompanha o porto de chegada inicialmente |
| `P3010-HU3-RN5-CN2` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | dados-pedido.spec.ts — edição manual da nacionalização é preservada |
| `P3010-HU3-RN5-CN3` | HOMOLOGADO NO CONTEXTO VALIDADO DE TRIBUTAÇÃO | impostos.e2e-spec.ts + pedido 9726 — tributação usa porto de nacionalização |
| `P3010-HU3-RN6-CN1` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | dados-pedido.spec.ts — proforma inicia com a invoice |
| `P3010-HU3-RN6-CN2` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | dados-pedido.spec.ts — proforma pode ser alterada manualmente |
| `P3010-HU3-RN7-CN1` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | dados-pedido.spec.ts — previsão de embarque inicia com a data da invoice |
| `P3010-HU3-RN7-CN2` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | dados-pedido.spec.ts — entrada no estoque é sugerida como chegada + 20 dias |
| `P3010-HU3-RN7-CN3` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | dados-pedido.spec.ts — entrada editada manualmente deixa de acompanhar a chegada |
| `P3010-HU3-RN8-CN1` | IMPLEMENTADO · VALIDADO POR TESTES · HOMOLOGAÇÃO A VALIDAR | ESP + gate técnico atual |
| `P3010-HU3-RN8-CN2` | IMPLEMENTADO · VALIDADO POR TESTES · HOMOLOGAÇÃO A VALIDAR | ESP + gate técnico atual |
| `P3010-HU3-RN8-CN3` | IMPLEMENTADO · VALIDADO POR TESTES · HOMOLOGAÇÃO A VALIDAR | ESP + gate técnico atual |
| `P3010-HU4-RN1-CN1` | IMPLEMENTADO · VALIDADO POR TESTES · HOMOLOGAÇÃO A VALIDAR | ESP + gate técnico atual |
| `P3010-HU4-RN2-CN1` | IMPLEMENTADO · VALIDADO POR TESTES · HOMOLOGAÇÃO A VALIDAR | ESP + gate técnico atual |
| `P3010-HU4-RN2-CN2` | IMPLEMENTADO · VALIDADO POR TESTES · HOMOLOGAÇÃO A VALIDAR | ESP + gate técnico atual |
| `P3010-HU4-RN2-CN3` | IMPLEMENTADO · VALIDADO POR TESTES · HOMOLOGAÇÃO A VALIDAR | ESP + gate técnico atual |
| `P3010-HU4-RN3-CN1` | IMPLEMENTADO · VALIDADO POR TESTES · HOMOLOGAÇÃO A VALIDAR | ESP + gate técnico atual |
| `P3010-HU4-RN3-CN2` | IMPLEMENTADO · VALIDADO POR TESTES · HOMOLOGAÇÃO A VALIDAR | ESP + gate técnico atual |
| `P3010-HU4-RN4-CN1` | IMPLEMENTADO · VALIDADO POR TESTES · HOMOLOGAÇÃO A VALIDAR | ESP + gate técnico atual |
| `P3010-HU4-RN5-CN1` | IMPLEMENTADO · VALIDADO POR TESTES · HOMOLOGAÇÃO A VALIDAR | ESP + gate técnico atual |
| `P3010-HU4-RN5-CN2` | IMPLEMENTADO · VALIDADO POR TESTES · HOMOLOGAÇÃO A VALIDAR | ESP + gate técnico atual |
| `P3010-HU4-RN6-CN1` | IMPLEMENTADO · VALIDADO POR TESTES · HOMOLOGAÇÃO A VALIDAR | ESP + gate técnico atual |
| `P3010-HU4-RN6-CN2` | IMPLEMENTADO · VALIDADO POR TESTES · HOMOLOGAÇÃO A VALIDAR | ESP + gate técnico atual |
| `P3010-HU4-RN7-CN1` | IMPLEMENTADO · VALIDADO POR TESTE · HOMOLOGAÇÃO A VALIDAR | ESP + gate técnico atual |
| `P3010-HU4-RN7-CN2` | IMPLEMENTADO · VALIDADO POR TESTE · HOMOLOGAÇÃO A VALIDAR | ESP + gate técnico atual |
| `P3010-HU5-RN1-CN1` | HOMOLOGADO NO CONTEXTO VALIDADO DE TRIBUTAÇÃO | VALIDACAO_HOMOLOGACAO_RODADAS.md + impostos.e2e-spec.ts — contexto válido retorna tributação |
| `P3010-HU5-RN1-CN2` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | impostos-item.spec.ts + gravacao.service.spec.ts — item sem tributação utilizável é recusado |
| `P3010-HU5-RN2-CN1` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | impostos-item.spec.ts — PIS/COFINS usam PCEXPISCOFINSITEM quando há exceção |
| `P3010-HU5-RN2-CN2` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | impostos-item.spec.ts — ausência de exceção mantém tributação normal |
| `P3010-HU5-RN3-CN1` | HOMOLOGADO NO CASO VALIDADO DO ITEM 9018 | trace do pedido 11681 + impostos.e2e-spec.ts — II/PERCIMPORTACAO |
| `P3010-HU5-RN3-CN2` | HOMOLOGADO NO CASO VALIDADO DO ITEM 9018 | trace do pedido 11681 + impostos.e2e-spec.ts — IPI/PERIPI |
| `P3010-HU6-RN1-CN1` | HOMOLOGADO NO ESCOPO VALIDADO DO PRIMEIRO PEDIDO | VALIDACAO_HOMOLOGACAO_RODADAS.md — 71/71 itens + calculo.e2e-spec.ts |
| `P3010-HU6-RN1-CN2` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | calculo.service.spec.ts — PESOLIQDI obrigatório ausente em cenário com despesa gera pendência e podeUsar=false |
| `P3010-HU6-RN2-CN1` | HOMOLOGADO NO ESCOPO VALIDADO DO PRIMEIRO PEDIDO | VALIDACAO_HOMOLOGACAO_RODADAS.md |
| `P3010-HU6-RN2-CN2` | HOMOLOGADO NO ESCOPO VALIDADO DO PRIMEIRO PEDIDO | VALIDACAO_HOMOLOGACAO_RODADAS.md |
| `P3010-HU6-RN3-CN1` | HOMOLOGADO NO ESCOPO ATUAL DO PRIMEIRO PEDIDO | VALIDACAO_HOMOLOGACAO_RODADAS.md |
| `P3010-HU6-RN3-CN2` | HOMOLOGADO NO ESCOPO ATUAL DO PRIMEIRO PEDIDO | VALIDACAO_HOMOLOGACAO_RODADAS.md |
| `P3010-HU6-RN4-CN1` | HOMOLOGADO PARA CONSIDERAESTPENDSUGCOMPRA=N · RAMO S NÃO HOMOLOGADO | ROTEIRO_QTSUGESTAO.md + pedido 11866 |
| `P3010-HU6-RN4-CN2` | HOMOLOGADO PARA CONSIDERAESTPENDSUGCOMPRA=N · RAMO S NÃO HOMOLOGADO | ROTEIRO_QTSUGESTAO.md + pedido 11866 |
| `P3010-HU6-RN4-CN3` | HOMOLOGADO PARA CONSIDERAESTPENDSUGCOMPRA=N · RAMO S NÃO HOMOLOGADO | ROTEIRO_QTSUGESTAO.md + pedido 11866 |
| `P3010-HU7-RN1-CN1` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | gravacao.service.spec.ts + gravacao.e2e-spec.ts — GRAVACAO_3010_ATIVA desligada retorna 403 |
| `P3010-HU7-RN1-CN2` | HOMOLOGADO NA TESTE PARA O PRIMEIRO PEDIDO | VALIDACAO_PRIMEIRO_PEDIDO_GRAVADO.md — pedido 11858 gravado com habilitação explícita |
| `P3010-HU7-RN2-CN1` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | gravacao.service.spec.ts — servidor refaz e confere os dados antes da escrita |
| `P3010-HU7-RN2-CN2` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | gravacao.service.spec.ts — inconsistências de filial, fornecedor, tributação e demais dados bloqueiam antes do Oracle |
| `P3010-HU7-RN3-CN1` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | gravacao.oracle.spec.ts — sequência connect → begin → commit → release |
| `P3010-HU7-RN3-CN2` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | gravacao.oracle.spec.ts — falha intermediária executa rollback e desfaz a operação |
| `P3010-HU7-RN4-CN1` | HOMOLOGADO NA TESTE PARA O PRIMEIRO PEDIDO | VALIDACAO_PRIMEIRO_PEDIDO_GRAVADO.md — NUMPED 11858 e master 1049/0426 |
| `P3010-HU7-RN4-CN2` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | gravacao.oracle.spec.ts — NUMPED ou master já existente é recusado com rollback |
| `P3010-HU7-RN4-CN3` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | gravacao.oracle.spec.ts — master existente é preservado e nenhum DELETE é executado |
| `P3010-HU7-RN5-CN1` | HOMOLOGADO NA TESTE PARA O PRIMEIRO PEDIDO | VALIDACAO_PRIMEIRO_PEDIDO_GRAVADO.md |
| `P3010-HU7-RN5-CN2` | HOMOLOGADO NA TESTE PARA O PRIMEIRO PEDIDO | VALIDACAO_PRIMEIRO_PEDIDO_GRAVADO.md |
| `P3010-HU7-RN5-CN3` | HOMOLOGADO NA TESTE PARA O PRIMEIRO PEDIDO | VALIDACAO_PRIMEIRO_PEDIDO_GRAVADO.md |
| `P3010-HU7-RN6-CN1` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | gravacao.oracle.spec.ts — blocos PCFORNEC, PCPRODUT e PCPRODFILIAL executam antes do commit |
| `P3010-HU7-RN6-CN2` | IMPLEMENTADO · VALIDADO POR TESTES AUTOMATIZADOS | gravacao.oracle.spec.ts — falha antes da conclusão provoca rollback e impede commit |

## Resumo da migração

- Cenários existentes na ESP: **85**.
- Cenários com estado reconciliado nesta matriz: **85**.
- Cenários ainda a reconciliar: **0**.

Os **85 critérios de aceite estão reconciliados com alguma evidência conhecida**. Isso não significa que os 85 estejam homologados:
cada linha preserva a distinção entre homologação funcional, validação por testes automatizados e comportamento apenas confirmado por inspeção do código.
