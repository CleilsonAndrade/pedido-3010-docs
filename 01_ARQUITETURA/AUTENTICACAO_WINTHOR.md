# Arquitetura — Autenticação com o usuário do WinThor

## 1. Login

```text
POST /api/v1/auth/login        { username, password }
```

```text
PCEMPR onde
  USUARIOBD (sem espaço, maiúsculo) = usuário digitado
  e a senha confere pela função CRYPT do próprio WinThor
      |
      v
setor = AUTH_REQUIRED_COD_SECTION (18 = IMPORTACAO, rotina 528)    senão 403
área  = AUTH_REQUIRED_AREA_ACTING, só quando configurada
      |
      v
JWT (JWT_SECRET, validade JWT_EXPIRATION_TIME, 60m)
```

A senha nunca é guardada nem registrada em log.

## 2. O que o token leva

```text
subject        winthor:<matrícula>
registration   PCEMPR.MATRICULA  -> CODFUNC, CODFUNCINCLUSAO, CODFUNCALTERACAO,
                                    PCITEM.CODFUNCALTER, e o :MATRICULA do bloco do PCPRODUT
username       PCEMPR.USUARIOBD  -> PCPEDIDO.FUNCLANC
name, roles    exibição e setor/área
```

As filiais do usuário vêm da PCLIB pela matrícula: a gravação recusa filial que
não esteja liberada para quem grava.

## 3. Rotas

Todas exigem o token (`JwtAuthGuard`), menos o login e a saúde. Na tela, a sessão
fica na aba (`sessionStorage`); token vencido (401) volta para a entrada.
