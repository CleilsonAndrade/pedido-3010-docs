# Operação — Configuração e execução

## 1. Variáveis (`api/.env`, modelo em `.env.example`)

```text
NODE_ENV                    development | production | test
LOG_LEVEL                   info (padrão)
PORT                        3010
DB_HOST, DB_PORT            homologação: 172.20.20.13, 1521
DB_USERNAME, DB_PASSWORD    usuário Oracle da aplicação
DB_SERVICE_NAME             homologação: TESTE (não CDBTST)
JWT_SECRET                  chave grande, por ambiente
JWT_EXPIRATION_TIME         60m
AUTH_REQUIRED_COD_SECTION   18 (IMPORTACAO, rotina 528)
AUTH_REQUIRED_AREA_ACTING   vazio = só o setor
COMEX_API_URL               http://127.0.0.1:8000  (127.0.0.1, não "localhost")
COMEX_API_TIMEOUT_MS        120000
GRAVACAO_3010_ATIVA         N = só prévia; S = grava (só na máquina de teste, por ora)
```

A subida recusa `.env` inválido ou incompleto. Os valores reais não são
versionados nem documentados. O `.env` só é lido quando a API sobe: mudou,
reinicie.

## 2. Rodar (três terminais)

```bash

# 1. comex (a senha dos LASTs fica só neste terminal)

cd ~/ww/comex-api && source .venv/bin/activate
printf 'Senha dos LASTs: '; read -rs PLANILHA_SENHA; echo; export PLANILHA_SENHA
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000

# 2. API

cd ~/ww/pedido-3010/api
fuser -k 3010/tcp 2>/dev/null        # derruba uma API antiga, se houver (EADDRINUSE)
npm run start:dev                    # http://127.0.0.1:3010/api/docs

# 3. tela

cd ~/ww/pedido-3010/web && npm start # http://localhost:4200
```

```bash
curl -s http://127.0.0.1:3010/api/v1/saude     # {"status":"ok","banco":true,"comex":true}
```

Ligar e desligar a gravação na máquina de teste:

```bash
sed -i 's/^GRAVACAO_3010_ATIVA=.*/GRAVACAO_3010_ATIVA=S/' ~/ww/pedido-3010/api/.env
sed -i 's/^GRAVACAO_3010_ATIVA=.*/GRAVACAO_3010_ATIVA=N/' ~/ww/pedido-3010/api/.env
```

## 3. Testes (gate)

```bash
cd api
npx jest                                  # unidade
npx jest --config ./test/jest-e2e.json    # ponta a ponta
npx tsc --noEmit -p tsconfig.json && npx eslint src && npm run build
cd ../web && npm test && npm run build
sh scripts/regra-regressao.sh --intervalo <inicio> HEAD
```

Os números atuais do gate estão em `00_STATUS/STATUS_PEDIDO_3010.md` (seção 3).

Ensaio com um lote inteiro de LASTs (comex no ar):

```bash
PLANILHAS_DIR=/pasta/com/lasts COMEX_API_URL=http://127.0.0.1:8000 \
  npx jest --config ./test/jest-e2e.json
```

## 4. Regras do repositório do código

```text
fix sem teste de regressão   recusado (gancho commit-msg local E no CI);
                             a mensagem do commit diz "Teste de regressão: <arquivo>"
rota sem Swagger             um teste falha
rota nova que escreve        o teste da documentação falha (só a gravação escreve)
instalar o gancho            sh scripts/instalar-ganchos.sh (uma vez por máquina)
```

## 5. Patches e GitHub

As mudanças chegam como **patches numerados** (`0001` a `0053` em 25/09),
aplicados em ordem com `git am`. A sincronia entre as máquinas é **pelo
GitHub**:

```text
aplique cada patch SÓ na máquina em que você estiver, e faça git push em seguida
na outra máquina, comece sempre por git pull --rebase
o --rebase descarta sozinho commit que traz a mesma mudança já no GitHub
```

```bash
cd ~/ww/pedido-3010
git am /mnt/c/Users/cleilson.andrade/Downloads/00NN-*.patch
git push
git --no-pager log --oneline -3
```

Comandos git que mostram saída vão **sempre com `--no-pager`** (ou, de uma vez:
`git config --global core.pager cat`). O push na `master` roda o CI (e o CD,
quando o runner estiver configurado).

Arquivo baixado de novo com o mesmo nome vira `NOME (1).md` no Windows:
para pegar o mais novo, `ls -t "$D"/NOME*.md | head -1`.
