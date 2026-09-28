# Arquitetura — Visão Geral

## 1. Componentes

```text
navegador
   |
   v
tela (Angular 21, web/)            publicação própria; chama /api por caminho relativo
   |
   v
pedido-3010 API (NestJS 11)        porta 3010, PM2, srv-fedora-r450
   |
   |-- comex-api (Python)          lê os LASTs: POST /api/v1/import-documents/leitura
   |
   `-- Oracle 19c do WinThor       TypeORM, conexão "winthor_conn"
          |
          `-- rotina 3010 (Gerenciar Importação [Pedido Máster])
```

## 2. Módulos da API (`api/src/`)

```text
auth/                 login WinThor (setor 18), JWT; RolesGuard e JwtAuthGuard
modules/comex/        cliente HTTP do comex-api (contrato em comex.contrato.ts)
modules/previa/       POST /previa e as regras (código × descrição, negociação,
                      itens repetidos, avisos, ocorrências do comex)
modules/cadastros/    GET /cadastros/* (listas do WinThor, cotação, impostos,
                      sugestão e validação da negociação)
modules/winthor/      consultas Oracle SOMENTE LEITURA (de-para, cadastros,
                      impostos do item, pedidos da invoice)
modules/calculo/      impostos, custo, rateio de despesas e VLTOTAL; POST /calculo/pedido
modules/gravacao/     POST /gravacao: montagem das 309 colunas e a execução (a única
                      parte que escreve)
modules/saude/        GET /saude (Oracle + comex)
common/observability/ id de rastreio por requisição, log operacional
```

## 3. Princípios

```text
nada grava sem prévia     a gravação refaz a prévia do mesmo arquivo (SHA-256)
o servidor não confia     cotação, tributação, cadastros e escolhas conferidos de novo
  na tela                 no servidor antes de gravar
igual à 3010              colunas, fixos, blocos PL/SQL e efeitos colaterais como a
                          3010 grava; os dois desvios são de segurança (uma transação
                          só; não apagar pelo NUMPED)
só uma rota escreve       POST /gravacao, atrás da chave GRAVACAO_3010_ATIVA; um teste
                          da documentação falha se outra rota escrever
datas nunca como Date     sempre texto + TO_DATE(:n, 'YYYY-MM-DD') (o fuso já fez a
                          cotação cair no dia anterior)
evidência antes de regra  regra nova sai de dado real do banco, do trace ou de LAST real
```

## 4. Etapas do projeto

```text
etapa 1   prévia (só leitura)                                   feita
etapa 2   tela de conferência                                   partes 1 a 5 feitas
etapa 3   gravação do 1º pedido na 3010                         feita, validada na homologação
etapa 4   produção, com a chave ligada por decisão              pendente (QTSUGESTAO)
```

A arquitetura segue a do `amazon-winthor-integration`: login WinThor, logs com id
de rastreio, validação do `.env` na subida, PM2.
