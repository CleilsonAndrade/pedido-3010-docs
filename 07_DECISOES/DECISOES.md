# Arquitetura — Decisões

**Natureza:** decisão. Cada linha diz de onde veio: do Cleilson, do time da
importação, ou de evidência (banco, trace, homologação). Decisão que muda
comportamento vira teste no repositório do código.

A coluna **#** mantém a numeração original das decisões de 22/09 (1 a 12, A e D),
citada nos commits e nos testes.

| # | Assunto | Decisão | De onde veio |
|---|---|---|---|
| — | Leitura | comex-api em Python, sem reescrever | `PROCESSO_EMISSAO_INVOICE.md` do próprio comex |
| — | PCOMPRA | Preço **arredondado da invoice**, não o do LAST | Cleilson: o time lança o que sai na invoice |
| 1 | NUMINVOCE | Invoice do LAST (`26MMC709F`) | 30 últimos pedidos da 3010 |
| 1 | NUMPROFORMA | Igual ao NUMINVOCE | 25 de 30 iguais; os 5 diferentes são sobra do pedido anterior |
| 1 | NUMNEGOCIACAO | Ano da invoice + sequência. Sugere maior da 3010 no ano + 1, editável | `04_VALIDACOES/EVIDENCIAS_TRACE_E_BANCO.md` |
| A | Validar negociação | Bloqueia vazio, 0, teste (1111, 11111, 1234...); avisa 4 dígitos, outro tamanho que não 5 (602, 266022) ou ano ≠ invoice | Cleilson |
| 2 | Planilha x pedido | 1 planilha = 1 pedido | Cleilson |
| 3 | Impostos | Vêm do cadastro tributário (como a tela), usuário confere | trace |
| 4 | Efeitos colaterais | Atualizar PCPRODUT, PCFORNEC, PCPRODFILIAL **igual à 3010** | trace + Cleilson |
| 5 | Fornecedor | Usuário escolhe sempre (a planilha só traz o nome) | Cleilson |
| 6 | IDPEDIDOMASTER | Numerador PCNUMERADORIMP. Só o 1º pedido (ver `04_VALIDACOES/EVIDENCIAS_TRACE_E_BANCO.md`). **Texto**, ex.: `1046/0426` | banco + homologação |
| 7 | VLTOTAL | **Em reais, com impostos**, calculado como a tela | trace: 619.353,60 |
| 8 | Código x descrição | Avisa e trava até o usuário escolher | Cleilson |
| 9 | Acesso | Setor 18 (IMPORTACAO) no PCEMPR | print da rotina 528 |
| 10 | Desfazer | Permitido enquanto não houver entrada | Cleilson |
| 11 | Testes | Primeiro na MIMO-HOMOLOG (172.20.20.13, serviço TESTE) | Cleilson |
| 12 | Servidor | srv-fedora-r450, PM2, porta 3010, app em `/home/admin/apps/pedido-3010` | Cleilson |
| D | Fornecedor + invoice repetidos | Avisa e deixa seguir, **com motivo obrigatório** | Cleilson |
| — | Pedido sem item | NUNCA grava (a 3010 não mostra master sem PCITEM) | teste do template |
| — | Backup | CI: `.bundle` do código (30 cópias). CD: versão no ar em `.tar.gz` (10 cópias) antes de trocar; sem backup não troca | Cleilson + scripts do .40 |
| — | Gravação | Chave `GRAVACAO_3010_ATIVA=N` até a etapa 3 estar aprovada | projeto |
| — | Tela | Aplicação Angular **separada da API**, não servida pelo NestJS | conversa da etapa 2 |
| — | Porto da tributação | **Porto de nacionalização** (PCPEDIDO.CODPORTONACIONALIZACAO), não o de chegada | homologação: pedido 9726, 6/6 × 0/6 |
| — | VLTOTAL do 1º pedido | Regra "parcela × QT a 2 casas"; **diferença de até 2 centavos aceita** (8 de 11 exatos, 3 a 1-2 centavos: arredondamento da própria tela). O contas a pagar nasce do 2º pedido | Cleilson, 24/09 |
| — | Filial e comprador na tela | Aplicar filial `4` e comprador `201` como defaults quando estiverem disponíveis ao usuário; não forçar default inexistente e manter ambos editáveis | implementação `89e1883` + `P3010-HU3-RN1` |
| — | Cotação USD do dia | Consultar BCB/PTAX, preferir fechamento do dia e aplicar acréscimo de 5%; escrita automática no WinThor somente com `COTACAO_BCB_GRAVACAO_ATIVA` habilitada; cotação histórica não é sobrescrita | implementação `2acd70e`/`3f3b652` + `P3010-HU4` |
| — | Cronologia das datas | Recusar chegada anterior ao embarque e entrada anterior à chegada; datas iguais são permitidas; validação existe na tela e na API | implementação `a5362cd` + `P3010-HU3-RN8` |
| — | QTSUGESTAO | **Calcular como a 3010 no caminho homologado**: `QTGIRODIA × (PRAZOENTREGA + TEMREPOS) − ESTOQUE_DISPONIVEL`; preservar resultado negativo; `QTVEZES` não entra na conta-base observada; filial com `CONSIDERAESTPENDSUGCOMPRA='S'` é recusada até esse ramo ser homologado | homologação 30/09, pedido 11866 |
| — | PCFORNECFILIAL na gravação | **Igual à 3010**: todos os fornecedores nas filiais que faltam (fora a 99) | Cleilson, 24/09 |
| — | Motivo da invoice repetida | **Nos dois**: **OBS7** ("Invoice repetida: ...", 100 caracteres; OBS4, OBS6 e OBS7 nunca usadas em 2026) e log da aplicação | Cleilson, 24 e 25/09 |
| — | Item repetido no LAST | Uma linha só por produto, com a quantidade somada; preços diferentes vão pela **média ponderada** (mantém o total da invoice), com aviso mostrando os preços e a média | Time da importação, 25/09 |
| — | Peso líquido da DI | **N.W. da linha ÷ quantidade** (o peso da invoice); o cadastro só quando o LAST não traz | Time da importação, 25/09 |
| — | Avisos do comex na prévia | Saem: contêiner, porto de embarque, cliente, imagem dos dados bancários. Ficam: total FOB (sem bloquear), nome da fábrica, porto de destino, data da invoice | Time da importação, 25/09 |
| — | Peso do LAST × cadastro | **Aviso** (não bloqueia) quando o peso do LAST difere **mais de 10%** do cadastro, para cima ou para baixo | Time da importação, 25/09 |
| — | Prioridade da etapa 3 | 1º pedido **sem frete** primeiro, com os impostos do cadastro; edição de impostos e despesas depois | Cleilson, 24/09 |
| — | Da prévia para a gravação | A tela guarda os arquivos e reenvia no "Gravar" com as escolhas; o servidor lê de novo, confere o SHA-256 e grava | Cleilson, 24/09 |
| — | Cabeçalho do 1º pedido | FRETE C, TIPOVENC P, TIPOEMBALAGEMPEDIDO V, PERCAPRAZO 100 fixos; fabricante e produtor = fornecedor; países = origem; só a previsão de chegada é digitada | roteiro 2.23, 25/09 |
| — | Restrições da tela | Produto que a 3010 esconderia na grade (sem tributação, fora de linha, proibido para venda, sem preço na região...) **trava** o item (`podeUsar` false) | Cleilson |

## Decisões que ainda faltam

```text
qual ação da 3010 gera o 2º pedido do master (não bloqueia o 1º)
onde a 3010 guarda os totais de frete e despesas (precisa de trace)
QTSUGESTAO com CONSIDERAESTPENDSUGCOMPRA='S': homologar esse ramo antes de habilitar
custo com o frete em dólar sem converter: replicar (hoje) ou corrigir (avisar o time)
```
