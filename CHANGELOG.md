# Changelog — Documentação do pedido-3010

## 2026-10-07 — Estado documental e gate atualizados

- Documentação alinhada ao código `pedido-3010 @ 51346d6`.
- BCB/PTAX + 5% implementado em `2acd70e`; proteção da gravação concorrente da cotação em `3f3b652`.
- Defaults operacionais de filial `4` e comprador `201`, quando disponíveis e sempre editáveis, implementados em `89e1883`.
- Cronologia das datas previstas implementada e coberta por testes na tela e na API em `a5362cd`; o pedido `11869` permanece somente como evidência do comportamento incorreto anterior à correção.
- `51346d6` restaurou o gate completo da API após as mudanças de cotação.
- Gate atual: API lint, 349/349 testes unitários, 48 E2E aprovados + 2 pulados, build e `diff --check`; tela com 76/76 testes e build aprovado.
- As evoluções posteriores ao baseline funcional `b813ceb` continuam aguardando homologação funcional na base TESTE.
- O checkpoint de 25/09 deixou de fazer parte da fotografia atual do STATUS e permanece preservado como histórico e nas validações específicas.
- A seção permanente de modo de trabalho foi movida do STATUS para o README.
- Criada `04_VALIDACOES/MATRIZ_VALIDACAO.md`, inicialmente rastreando os 85 critérios de aceite da ESP sem inferir estados não sustentados pelos documentos.

## 2026-09-30 — QTSUGESTAO homologada e implementada

- Pedido nativo **11866**, lançado pela própria 3010 na TESTE, reproduziu a
  conta-base em **2 de 2 itens**.
- Regra homologada para filial que não considera estoque pendente:
  `QTGIRODIA × (PRAZOENTREGA + TEMREPOS) − ESTOQUE_DISPONIVEL`.
- `QTVEZES` não entrou na conta-base observada; teste manual com valor 2 manteve
  o mesmo estoque ideal e a mesma `QTSUGESTAO`.
- Testes manuais também confirmaram a sobrescrita de prazo e tempo de reposição
  quando esses valores são informados na tela da 3010.
- A implementação usa `PCEST.QTGIRODIA`, `PCFORNEC.PRAZOENTREGA`,
  `PCPRODUT.TEMREPOS` e
  `PKG_ESTOQUE.ESTOQUE_DISPONIVEL(CODPROD, CODFILIAL, 'C')`.
- Resultado negativo é preservado.
- Filial com `CONSIDERAESTPENDSUGCOMPRA='S'` continua não homologada e é recusada
  pela API em vez de receber regra presumida.
- Código: `c96e389` e `b813ceb`.
- Homologação final do `b813ceb`: **16 ok · 5 diferente · 0 erro · 17 info ·
  2 pulado**; item 2.24 reproduziu 2/2 itens.

## 2026-09-28 — Roteiro de descoberta da QTSUGESTAO (0055)

- Preparado o item 2.24 do roteiro, acionado por `NUMPED_QTSUGESTAO`, para um
  pedido lançado manualmente pela 3010 na TESTE.
- O item é somente leitura: coleta a QTSUGESTAO gravada, estoque, giro, pendência,
  prazo de entrega, tempo de reposição, mínimo e múltiplo, infere `QTVEZES` com e
  sem pendente e testa um fator comum em todos os itens.
- A fórmula permanece **hipótese** até uma rodada real; a aplicação continua com
  `QTSUGESTAO = 0` provisório e a produção continua bloqueada.
- Procedimento e critério de aceitação em
  `04_VALIDACOES/ROTEIRO_QTSUGESTAO.md`.

## 2026-09-28 — Repositório documental próprio

- A documentação saiu da pasta `docs/` do repositório do código para este
  repositório, `pedido-3010-docs`, no padrão do `amazon-winthor-integration-docs`:
  `00_STATUS` a `05_OPERACAO`, README com cabeçalho de controle e ordem de
  leitura, CHANGELOG e o consolidado gerado por `tools/regenerate_consolidated.py`.
- O `CONTINUAR.md` foi substituído pelo `00_STATUS/STATUS_PEDIDO_3010.md`, que
  inclui como retomar o projeto num chat novo.
- As rodadas de homologação (§3 do antigo CONTINUAR) e as evidências do trace e
  do banco (§5) viraram registro histórico em `03_VALIDACOES/`, com os ponteiros
  trocados para os documentos novos.
- A especificação da gravação foi dividida: fluxo (`02_FLUXOS`), validações
  (`03_VALIDACOES`), as 309 colunas (`04_CONTRATOS`) e os roteiros da base TESTE
  (`05_OPERACAO`).
- Corrigido: o serviço da homologação é **TESTE** (textos antigos diziam CDBTST).
- Registrado o que estava só na conversa de 25/09: as telas da 3010 com o 11858, o
  trace da abertura do pedido (sem escrita; itens travados com FOR UPDATE NOWAIT),
  o histórico de pesos dos 6 produtos do 26MSR296F e o roteiro de limpeza da TESTE
  com as lições (gatilho do PCITEMLOG, DDL confirma sozinho, itens órfãos).
- Os 7 pedidos sem item de testes do template (10483 a 10490), que eram um ponto
  em aberto, aparecem como apagados.
- No repositório do código, o patch **0054** tira a documentação de `docs/` (fica
  um apontador), deixa o README curto e atualizado, troca as referências antigas no
  código (comentários, Swagger, roteiro) e corrige o `.env.example` (serviço TESTE).
  O CUSTOULTENT deixou de aparecer como "em aberto" no Swagger: foi fechado na 3ª
  rodada.

## 2026-09-25 — Gravação do 1º pedido e validação do time (0038 a 0053)

- Roteiro 2.23: como a 3010 grava o cabeçalho do 1º pedido em 2026 (FRETE C,
  TIPOVENC P, embalagem V, 100% a prazo em 767 de 775; OBS4, OBS6 e OBS7 nunca
  usadas; proforma = invoice em 1.300 de 1.389) (0038, 0039).
- Invoice gravada com tabulação escapava da checagem de invoice repetida:
  `REGEXP_REPLACE` no lugar do `TRIM` (0040).
- Gravação: montagem das 309 colunas com teste de ouro (0041), execução numa
  transação só (0042), rota `POST /gravacao` conferindo tudo no servidor (0043),
  peso PESOLIQ quando falta o PESOLIQDI (0044), SHA-256 na prévia (0045), tela da
  gravação com confirmação (0046), numerador travado vira recusa clara (0047).
- Numerador de master da TESTE acertado de 406 para 1049.
- **Primeiro pedido gravado pela aplicação: 11858, master 1049/0426**; conferido
  no banco e na 3010.
- Motivo da invoice repetida decidido: OBS7 e log da aplicação.
- Validação do time com 3 LASTs: avisos que não bloqueiam (0048), item repetido
  somado e peso do LAST (0049), avisos na tela (0050), total FOB (0051), avisos do
  comex dispensados (0052), aviso de peso acima de 10% (0053).
- Pedidos 11859 a 11861 apagados da TESTE para o reteste.

## 2026-09-24 — Cálculo do 1º pedido fechado e tela, partes 1 a 4 (0016 a 0037)

- Rodadas 4ª a 12ª: frete e despesas do 1º pedido deduzidos do 11841 (a hipótese
  "frete só no 2º pedido" caiu na 6ª rodada); AFRMM como total informado; VLTOTAL
  pela regra "parcela × QT a 2 casas", com tolerância de 2 centavos decidida.
- 17ª rodada: o backend inteiro contra a homologação (21 ok).
- Rota de cálculo `POST /calculo/pedido` (0027).
- Tela em `web/` (Angular 21): entrar e conferir LASTs (0029), escolher o produto
  na linha trocada e no ambíguo (0030), pedido já lançado agrupado por master
  (0033, 0034), dados do pedido (0035), negociação pela regra A (0037).
- Especificação da gravação conferida contra o template (PCITEM 97 de 100,
  PCPEDIDO 96 de 100 iguais ao trace).

## 2026-09-23 — Homologação começa (0001 a 0015)

- Cotação caía no dia anterior (data ia ao Oracle como `Date`): datas passam a ir
  como texto em `TO_DATE` (0001).
- Regra A da negociação (0002, 0003), pedidos com a mesma invoice (0004), impostos
  do cadastro por item (0005), roteiro de homologação (0006).
- Rodadas 1ª a 3ª: IDPEDIDOMASTER é texto (0007); tributação pelo porto de
  nacionalização (0010); CUSTOULTENT do PCEST no 1º pedido; frete rateado por
  PESOLIQDI × QT (0014).

## 2026-09-22 — Etapa 1 (prévia) e decisões iniciais

- Decisões 1 a 12, A e D (`07_DECISOES/DECISOES.md`).
- Prévia só de leitura: login WinThor (setor 18), leitura pelo comex, de-para,
  regra código × descrição, cadastros.
