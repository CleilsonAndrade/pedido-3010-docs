# Contrato — Rotas da API pedido-3010

Base: `http://<servidor>:3010/api/v1`. Swagger em `/api/docs`; **um teste falha se
alguma rota ficar sem documentação**, e outro se alguma rota além da gravação
escrever no banco.

## 1. Rotas

```text
POST /auth/login                          login WinThor (setor 18) -> token
GET  /saude                               Oracle + comex
POST /previa                              lê os LASTs; prévia com pendências e avisos (não grava)
POST /calculo/pedido                      calcula o 1º pedido como a 3010 grava (não grava)
POST /gravacao                            GRAVA o 1º pedido na 3010 (só com GRAVACAO_3010_ATIVA=S)
GET  /cadastros/filiais                   PCLIB do usuário
GET  /cadastros/fornecedores?busca=       FORNECIMPORTACAO 6/7 ou REVENDA 'X'
GET  /cadastros/compradores               setor PCCONSUM.CODSETORCOMPRADOR
GET  /cadastros/moedas
GET  /cadastros/cotacao?moeda&data        cotação por data (TO_DATE no Oracle, sem fuso)
GET  /cadastros/paises
GET  /cadastros/portos
GET  /cadastros/vias
GET  /cadastros/incoterms
GET  /cadastros/impostos?filial&fornecedor&pais&portoNacionalizacao&produtos
GET  /cadastros/negociacao/sugestao?invoice   maior da 3010 no ano + 1, e quem usou a última
GET  /cadastros/negociacao/validar?valor&invoice   regra A, sem banco
```

Todas exigem o token, menos `/auth/login` e `/saude`.

## 2. POST /gravacao

```text
arquivo   o mesmo LAST da prévia
pedido    JSON:
  sha256                 o que a prévia devolveu para o arquivo
  escolhas               { linha: CODPROD } para as linhas trocadas ou ambíguas
  filial, codfornec, comprador, negociacao, moeda, dataCotacao (AAAA-MM-DD),
  incoterm, via, pais, portoChegada, portoNacionalizacao,
  numproforma (vazio = a invoice),
  dtprevembarque, dtprevchegada, dtpreventradaestoque (AAAA-MM-DD),
  motivoRepetida         obrigatório se o fornecedor já tem master desta invoice
```

A tela não manda cotação nem tributação: o servidor lê as duas.

```text
201  { numped, idPedidoMaster, invoice }
400  arquivo ou JSON faltando; campo em formato errado (diz o campo)
403  gravação desligada
409  arquivo diferente do conferido; NUMPED ou master já existentes; numerador ocupado
422  { statusCode, message, problemas: [...] }
```

Regras em `02_FLUXOS/GRAVACAO_NA_3010.md`.

## 3. POST /previa

Resposta por arquivo: `02_FLUXOS/PREVIA_DOS_LASTS.md` (seção 7). `gravacaoAtiva`
diz à tela se a chave está ligada.
