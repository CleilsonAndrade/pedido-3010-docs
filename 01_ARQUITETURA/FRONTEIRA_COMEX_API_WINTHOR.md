# Arquitetura — Fronteira comex-api × pedido-3010 × WinThor

## 1. Quem é dono do quê

```text
comex-api (Python)
  - ler o .xls com senha (via LibreOffice) e o .xlsx
  - corrigir peso invertido, embutir encargo, arredondar o preço como na invoice
  - ocorrências da planilha (campos vazios, conta bancária, pagamento...)
  - emitir invoice e packing (outro uso, fora do pedido-3010)

pedido-3010 API
  - de-para código de fábrica -> CODPROD
  - regras do pedido: código × descrição, negociação (A), invoice repetida (D),
    itens repetidos, peso
  - quais ocorrências do comex importam para lançar o pedido
  - cálculo dos valores do 1º pedido
  - gravação na 3010 (uma transação só)

WinThor (Oracle)
  - numeradores (PCCONSUM, PCNUMERADORIMP)
  - cadastros: produto, fornecedor, tributação, cotação, estoque
  - blocos PL/SQL que a 3010 roda depois de gravar (copiados do trace)
  - gatilhos do PCITEM (TRG_PCITEMLOG, TRG_PCITEM_BIN, TRG_PCITEM_PCLISTAFALTA)
  - o 2º pedido do master (criado pela própria 3010 depois)
```

## 2. Regras de fronteira

- **O comex não muda por causa do pedido-3010.** Os avisos que o time não usa
  (contêiner, porto de embarque, cliente, imagem dos dados bancários) saem **na
  prévia do pedido-3010**; o comex continua avisando para quem gera a invoice.
- **O pedido-3010 não reimplementa a leitura.** O preço é o arredondado da
  invoice, que o comex já calcula (decisão: o time lança o que sai na invoice).
- **O pedido-3010 não reimplementa os blocos da 3010.** Os três blocos PL/SQL
  (PCFORNEC, PCPRODUT, PCPRODFILIAL) rodam com o mesmo texto do trace e os mesmos
  parâmetros (NUMPED, filial, matrícula).
- **Regra que vale para a invoice também** (ex.: código × descrição trocados) hoje
  está só no pedido-3010; levar para o comex está em aberto.

## 3. Conexões

```text
tela -> API          /api relativo (proxy no desenvolvimento; repasse no servidor da tela)
API -> comex         COMEX_API_URL = http://127.0.0.1:8000
                     (127.0.0.1, não "localhost": o Node tenta IPv6 e falha)
API -> Oracle        DB_HOST / DB_SERVICE_NAME; homologação = serviço TESTE em 172.20.20.13
```
