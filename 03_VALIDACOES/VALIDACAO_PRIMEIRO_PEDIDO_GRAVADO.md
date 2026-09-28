# Validação — Primeiro pedido gravado pela aplicação (11858)

**Natureza:** observado em runtime, na **homologação** (base TESTE). **Não
equivale a publicação em produção**: a API rodava na máquina do Cleilson, com
`GRAVACAO_3010_ATIVA=S` só no `.env` local.

## 1. O pedido

```text
data                25/09/2026
NUMPED              11858
IDPEDIDOMASTER      1049/0426
invoice             26MZC900F   (o LAST 26MZC289F com a invoice trocada, só a célula B17)
fornecedor          15268  ZHEJIANG ZHICHENG HOUSEWARE CO., LTD
filial              4
itens               3   (linhas 8 e 9 escolhidas na tela)
cotação             5,1696 (USD, 15/09/2026, lida do WinThor pelo servidor)
VLTOTAL             84.059,54
FUNCLANC            CLEILSON.ANDRAD
```

O LAST de teste foi montado a partir do original: aberto com a senha,
convertido para `.xlsx` pelo LibreOffice, **só a B17** trocada, fórmulas
recalculadas. Comparação célula por célula: 1.248 células, a única diferença é
a B17; total FOB 12.000,00 igual ao original.

## 2. Conferido no banco

```text
base, II (16,2%), IPI (6,5%), custo      batem até a 6ª casa refazendo a conta
VLTOTAL                                  84.059,54 = regra "parcela × QT a 2 casas"
FRETE / TIPOVENC                         C / P
datas previstas                          chegada 22/09, entrada 12/10 (chegada + 20)
OBS7                                     vazia (sem motivo)
PCNUMERADORIMP 2026                      1049 -> 1050
PCCONSUM.PROXNUMPED                      11858 -> 11859
PCPRODUT.CUSTOREP                        0,55 / 0,55 / 0,65 (preço em dólar), data do dia
```

O CUSTOREP atualizado prova que os três blocos PL/SQL da 3010 rodaram pela
conexão da API. Ficaram confirmados os três pontos que só a homologação mostrava:
parâmetros nomeados nos blocos, permissões do usuário da API e o gatilho do
PCITEM.

## 3. Conferido na própria 3010

Aberto na rotina 3010 (PCSIS3010 v.37.0.08.071), sem salvar:

- a pesquisa acha o pedido pelo número, com master, valor total, negociação e
  proforma;
- o cabeçalho mostra cada campo no lugar (fornecedor, comprador, os três
  países, produtor e fabricante, FOB, os portos, as datas, a cotação nas duas
  moedas, "Considera capatazia" marcado);
- o master aparece em **vermelho (bloqueado)** e o "Notificado" como
  **0 OUTROS FORNECEDORES**: é o mesmo estado que a 3010 deixa ao lançar
  (`DTLIBERA`, `CODFUNCLIBERA` e `CODFORNECNOTIF` vazios no INSERT do 11681);
- o trace da abertura: **nenhuma escrita** (só leituras e o `UPDATE PCROTINA`
  de contagem de uso), os itens carregados pela consulta que junta PCITEM,
  PCPRODUT e PCPRODFILIAL, e `SELECT ... FROM PCITEM WHERE NUMPED = 11858 FOR
  UPDATE NOWAIT`: **a 3010 trava os itens enquanto o pedido está aberto**.

## 4. A primeira tentativa (trava do numerador)

A primeira tentativa pegou a PCCONSUM travada por outra aplicação em teste:
o `FOR UPDATE WAIT 5` venceu (ORA-30006), a transação foi desfeita inteira (a
segunda tentativa pegou o mesmo 11858, nenhum número queimado), mas a tela
mostrou "Internal server error". **Corrigido com teste de regressão:** trava
vencida (ORA-30006 ou ORA-00054) num numerador vira recusa 409 dizendo qual
numerador está ocupado e que dá para tentar de novo.

## 5. O que ficou para trás neste pedido

O 11858 foi gravado **antes** da correção do peso (patch 0049): o 15710 foi com
0,104167 kg/un do cadastro, e o LAST diz 0,14375. Na TESTE, não precisa refazer.
O pedido fica na base como referência.
