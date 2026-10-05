# Operação — Servidor e publicação

**Natureza:** procedimento. **Ainda não executado na produção** (a API
não foi publicada; a tela não tem publicação).

## Preparar o srv-fedora-r450 (uma vez)

Mesmo servidor e mesmo padrão do comex-api: runner self-hosted, PM2.

### 1. Script de backup (como root)

O CI e o CD chamam o script **como root** (o `mount -t cifs` exige). Por isso ele
fica em `/root/scripts`, dono root — **nunca** aponte o sudoers para a cópia do
repositório, senão qualquer commit rodaria comandos como root.

```bash
sudo cp scripts/backup/backup_srv181.sh /root/scripts/
sudo chown root:root /root/scripts/backup_srv181.sh
sudo chmod 700 /root/scripts/backup_srv181.sh
```

Usa o mesmo `/root/.smbcredentials_srv181` dos backups do GLPI. Log em
`/var/log/backup_pedido3010.log`, com as frases "Iniciando" e
"finalizado com sucesso" que o `backup_resumo.sh` já sabe ler.

Para o log não crescer para sempre, some ao `/etc/logrotate.d/backup_glpi`:

```
/var/log/backup_pedido3010.log
```

### 2. Liberar só esse script para o usuário do runner

```bash
sudo visudo -f /etc/sudoers.d/backup-pedido3010
```

```
admin ALL=(root) NOPASSWD: /root/scripts/backup_srv181.sh
```

Conferir: `sudo -n -l /root/scripts/backup_srv181.sh` (como admin) deve responder sem pedir senha.

O script recusa subpasta com `..`, prefixo com símbolo, extensão diferente de
`.bundle`/`.tar.gz` e quantidade fora de 1–99 (testado em `scripts/backup/testar-backup.sh`).

### 3. Runner e secret

- Runner self-hosted em `/home/admin/actions-runner-pedido-3010`, como os outros.
- A aplicação mora em `/home/admin/apps/pedido-3010` (fora do `_work`).
- Secret `ENV_FILE_CONTENTS` no GitHub com o `.env` de produção. O CD recusa
  publicar se faltar `GRAVACAO_3010_ATIVA`.

### 4. Voltar uma versão à mão

Rápido (a anterior, no próprio servidor):

```bash
cd /home/admin/apps/pedido-3010
rm -rf dist && cp -a dist.anterior dist && pm2 reload ecosystem.config.js --env production
```

Mais antiga (do srv181): pegue o `deploy_pedido3010_DD_MM_AA_HHMM.tar.gz` em
`\\172.20.20.40\srv181$\pedido-3010\deploy`, extraia por cima da pasta e rode
`npm ci --omit=dev` e o `pm2 reload`.

Código (se o GitHub sumir): `git clone codigo_pedido3010_DD_MM_AA_HHMM.bundle pedido-3010`

## CI/CD: backup e publicação

Resumo do que os workflows do repositório do código fazem:

```
push em dev / staging / master
  ↓ CI: regra do teste de regressão → testes → compilar
  ↓ CI: .bundle com o histórico inteiro → \\172.20.20.40\srv181$\pedido-3010\codigo (30 cópias)
push em master com CI verde
  ↓ CD: versão no ar → dist.anterior + .tar.gz → srv181\pedido-3010\deploy (10 cópias)
  ↓ CD: sem backup, NÃO troca a versão
  ↓ CD: copia a nova, sobe no PM2, confere /api/v1/saude
  ↓ CD: não respondeu em 60s → volta a anterior sozinho
```
