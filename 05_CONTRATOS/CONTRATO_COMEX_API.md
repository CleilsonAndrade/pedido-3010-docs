# Contrato — pedido-3010 com o comex-api

## 1. Rota

```text
POST {COMEX_API_URL}/api/v1/import-documents/leitura
multipart, campo "arquivos" (um ou mais LASTs)
timeout COMEX_API_TIMEOUT_MS (padrão 120000)
```

A rota `/leitura` **não existe no comex original**: vem do patch
`comex-api-rota-leitura.patch` (aplicado com `git apply` no comex-api). Sem ele, o
comex responde **405** e a tela diz que o comex recusou a leitura. O patch
`comex-api-senha-fora-do-teste.patch` tirou a senha padrão dos testes do comex.

Configuração do comex (fora deste repositório):

```text
PLANILHA_SENHA   senha dos LASTs, só no ambiente do terminal que sobe o comex
host             127.0.0.1 (o Node tenta IPv6 com "localhost" e falha)
```

Não registrar a senha real neste repositório documental.

## 2. Resposta consumida (`api/src/modules/comex/comex.contrato.ts`)

```text
ComexLeitura    versao_nucleo, processos[]
ComexProcesso   arquivo_origem, pode_emitir, erro?, cabecalho, itens[], ocorrencias[]
ComexCabecalho  invoice_number, invoice_date, fornecedor_nome, fornecedor_endereco,
                porto_embarque, porto_destino, conteiner, conteiner_observacao,
                total_fob_last, total_fob_invoice, deposito, saldo, frete_maritimo
ComexItem       linha_origem, codigo_fabrica, descricao, ncm, unidade, quantidade,
                preco_unitario (arredondado como na invoice), preco_unitario_last,
                total, caixas, peso_bruto, peso_liquido (N.W. da LINHA, kg)
ComexOcorrencia severidade, nivel (bloqueio | conferir | informativo), codigo,
                mensagem, linha_origem, campo
```

`pode_emitir` é do uso do comex (emitir a invoice); o pedido-3010 não usa.

## 3. Ocorrências que o pedido-3010 trata (códigos do comex, `nucleo/validacao.py`)

```text
cabecalho.vazio / cntr_number       número do contêiner        dispensada (não aparece)
cabecalho.vazio / port_loading      porto de embarque          dispensada
cabecalho.vazio / to                cliente                    dispensada
conta.ausente   / imagem_conta      imagem dos dados bancários dispensada
cabecalho.vazio / total_fob_price   total FOB                  aparece, não bloqueia
                                                               (a tela soma e avisa)
cabecalho.vazio / factory_name      nome da fábrica            como o comex manda
cabecalho.vazio / port_discharge    porto de destino           como o comex manda
cabecalho.vazio / invoice_date      data da invoice            como o comex manda
demais                              nível "bloqueio" vira pendência BLOQUEIO_COMEX;
                                    os outros aparecem como ocorrência
```

Decisão do time da importação (25/09). Os rótulos vêm do dicionário `ROTULOS` do
comex (`cntr_number` = número do contêiner, `port_loading` = porto de embarque,
`to` = cliente, `total_fob_price` = total FOB, `factory_name` = nome da fábrica,
`port_discharge` = porto de destino, `invoice_date` = data da invoice).

## 4. Erros

```text
comex fora do ar / timeout   "O comex-api (leitura das planilhas) não respondeu."
405                          patch da rota /leitura não aplicado
processo.erro                pendência LEITURA_FALHOU no pedido daquele arquivo
```
