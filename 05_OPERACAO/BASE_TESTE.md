# Operação — Base TESTE (MIMO-HOMOLOG)

**Natureza:** procedimento, usado de verdade em 25/09. **Só na base TESTE.**
Todo roteiro começa conferindo a base:

```sql
SELECT SYS_CONTEXT('USERENV', 'SERVICE_NAME') FROM DUAL;   -- teste
```

Rode **uma instrução por vez** (no DBeaver, Ctrl+Enter em cada): duas juntas
numa execução dão ORA-00933.

## 1. Numeradores

A gravação usa dois:

```text
PCCONSUM.PROXNUMPED              NUMPED (todos os pedidos de compra)
PCNUMERADORIMP.PROXNUMPEDIDO     master do ano (IDPEDIDOMASTER "número/FFAA")
```

Conferir:

```sql
SELECT PROXNUMPEDIDO FROM PCNUMERADORIMP WHERE ANO = '2026';
SELECT MAX(TO_NUMBER(REGEXP_SUBSTR(IDPEDIDOMASTER, '^[0-9]+'))) FROM PCPEDIDO WHERE IDPEDIDOMASTER LIKE '%/__26';
SELECT PROXNUMPED FROM PCCONSUM;
SELECT MAX(NUMPED) FROM PCPEDIDO;
```

Acerto do master (maior em uso + 1, sem número digitado):

```sql
UPDATE PCNUMERADORIMP
   SET PROXNUMPEDIDO = (SELECT MAX(TO_NUMBER(REGEXP_SUBSTR(IDPEDIDOMASTER, '^[0-9]+'))) + 1
                          FROM PCPEDIDO WHERE IDPEDIDOMASTER LIKE '%/__26')
 WHERE ANO = '2026';
COMMIT;
```

Histórico: em 25/09 o master estava em 406 com 1048 em uso (a TESTE é cópia da
produção, mas o numerador não veio junto); acertado para 1049. O PCCONSUM
estava certo (11858 × 11857). **O PCCONSUM não se devolve**: numera todos os
pedidos de compra, e outra aplicação pode ter usado números depois.

## 2. LAST de teste

Um LAST real com a **invoice trocada** (mantendo o "26" do ano), para gravar sem
cair na decisão D. O LAST tem senha e preço de fornecedor: a troca é feita no
Excel do time (Localizar e substituir na pasta de trabalho inteira), ou abrindo
com a senha, trocando a célula e comparando célula por célula com o original
(como foi feito com o 26MZC900F). Apague a cópia depois do teste.

## 3. Primeiro pedido de teste (passo a passo)

1. No `api/.env` **da sua máquina** (base TESTE): `GRAVACAO_3010_ATIVA=S`.
   Nunca no servidor de produção antes de a QTSUGESTAO ser conferida.
2. Suba o comex (com a `PLANILHA_SENHA`), a API e a tela.
3. Solte o LAST de teste (26MPS900F: um LAST real com a invoice trocada).
4. Preencha comprador, data da cotação 15/09/2026 (5,1696 na TESTE) e a
   previsão de chegada; confira o resto.
5. "Gravar na 3010" → "Confirmar e gravar". Deve aparecer o NUMPED e o master
   (o primeiro deve ser `1049/0426`).
6. Confira no banco:
   ```sql
   SELECT NUMPED, IDPEDIDOMASTER, NUMINVOCE, CODFORNEC, VLTOTAL, FUNCLANC, OBS7
     FROM PCPEDIDO WHERE NUMPED = <o NUMPED que apareceu>;
   SELECT NUMSEQ, CODPROD, QTPEDIDA, PCOMPRA, BASEPISCOFINSLIT, VLIMPORTACAO, CUSTOULTPEDCOMPRA
     FROM PCITEM WHERE NUMPED = <o NUMPED> ORDER BY NUMSEQ;
   ```
   e abra o pedido na própria 3010: ele tem que aparecer como qualquer outro.
7. Se der erro, **nada fica gravado** (a transação é desfeita); o log da API
   diz o motivo. Erro de permissão (ORA-01031) quer dizer que o usuário da
   API precisa de INSERT/UPDATE nessas tabelas e EXECUTE no PARAMFILIAL.

## 4. Apagar pedido de teste

Usado para apagar 11859, 11860 e 11861 antes do reteste do time. Lições:
o gatilho `TRG_PCITEMLOG` (BEFORE DELETE OR UPDATE) grava o nome do programa
em `PCITEMLOG.PROGRAMA` (40 caracteres) e **barra o DELETE vindo do DBeaver**,
que se apresenta com um nome maior; `ALTER TRIGGER` **confirma sozinho** o que
estiver pendente (é DDL); apagar o PCPEDIDO sem o PCITEM deixa **itens órfãos**.

```sql
SELECT SYS_CONTEXT('USERENV', 'SERVICE_NAME') FROM DUAL;          -- teste
SELECT NUMPED, IDPEDIDOMASTER, NUMINVOCE, FUNCLANC FROM PCPEDIDO WHERE NUMPED IN (...);
SELECT (SELECT COUNT(*) FROM PCMOV WHERE NUMPED IN (...)) ENTRADAS,
       (SELECT COUNT(*) FROM PCITEM WHERE NUMPEDMASTERORIGEM IN (...)) SEGUNDO_PEDIDO FROM DUAL;  -- 0 e 0
ALTER TRIGGER MIMOTESTE.TRG_PCITEMLOG DISABLE;
ALTER TRIGGER MIMOTESTE.TRG_PCITEM_BIN DISABLE;
DELETE FROM PCITEM   WHERE NUMPED IN (...);                         -- conferir o número
DELETE FROM PCPEDIDO WHERE NUMPED IN (...);                         -- conferir o número
COMMIT;                                                             -- ou ROLLBACK
ALTER TRIGGER MIMOTESTE.TRG_PCITEMLOG ENABLE;                       -- SEMPRE, depois do COMMIT
ALTER TRIGGER MIMOTESTE.TRG_PCITEM_BIN ENABLE;
UPDATE PCNUMERADORIMP
   SET PROXNUMPEDIDO = (SELECT MAX(TO_NUMBER(REGEXP_SUBSTR(IDPEDIDOMASTER, '^[0-9]+'))) + 1
                          FROM PCPEDIDO WHERE IDPEDIDOMASTER LIKE '%/__26')
 WHERE ANO = '2026';
COMMIT;
SELECT TRIGGER_NAME, STATUS FROM ALL_TRIGGERS WHERE TABLE_NAME = 'PCITEM' AND OWNER = 'MIMOTESTE';  -- todos ENABLED
```

O **PCCONSUM não volta**: ele numera todos os pedidos de compra, e outra
aplicação pode ter usado números depois (o buraco na sequência não atrapalha).
Os blocos da 3010 que rodaram na gravação (CUSTOREP e PESOLIQDI do PCPRODUT,
PCPRODFILIAL, PCFORNEC, PCFORNECFILIAL) não são desfeitos: na TESTE, não precisa.

## 5. Estado da TESTE depois de 25/09

```text
11858 (1049/0426, 26MZC900F)     fica, como referência (peso do 15710 ainda do cadastro)
11859, 11860, 11861              apagados (itens e pedidos) para o reteste do time
PCNUMERADORIMP 2026              1050
PCCONSUM                         não devolvido (continua de onde estava)
gatilhos do PCITEM               os 3 ENABLED (TRG_PCITEM_BIN, TRG_PCITEMLOG,
                                 TRG_PCITEM_PCLISTAFALTA)
```

Lição de 25/09: apagar o PCPEDIDO com o DELETE do PCITEM barrado pelo gatilho
deixou **12 itens órfãos**; foram apagados depois com os gatilhos desligados.
Sempre apague o PCITEM **antes** e confira os dois números antes do COMMIT.
