# Validação — roteiro da QTSUGESTAO da rotina 3010

**Natureza:** procedimento de descoberta preparado; ainda sem resultado real
**Data de referência:** 2026-09-28
**Código que prepara o item:** `d3a0f53 feat: roteiro da QTSUGESTAO por NUMPED` (patch 0055)
**Bloqueio atual:** produção continua bloqueada; a aplicação continua gravando `QTSUGESTAO = 0` até esta conta ser fechada por evidência

---

## 1. Objetivo

Descobrir e confirmar, com um pedido **lançado manualmente pela própria 3010** na
base TESTE, a conta final que a rotina usa para gravar `PCITEM.QTSUGESTAO`.

O trace já mostrou a estrutura da sugestão, mas cortou os valores dos parâmetros
de prazo e do fator `QTVEZES`. Por isso este roteiro não transforma a hipótese em
regra: ele lê o resultado que a 3010 gravou e tenta reconstruir a conta para cada
item.

## 2. O que já é evidência do trace

```text
ESTOQUE        = PKG_ESTOQUE.ESTOQUE_DISPONIVEL(CODPROD, CODFILIAL, 'C')
QTGIRODIA      = giro diário (ESTCONSOLIDADO)
M_ESTIDEAL     = QTGIRODIA × (prazo de entrega + tempo de reposição) × QTVEZES
QTPENDENTE     entra quando PCFILIAL.CONSIDERAESTPENDSUGCOMPRA = 'S'
QTMINSUGCOMPRA e MULTIPLOCOMPRAS participam do caminho da sugestão
```

No pedido do trace, o produto 9018 ficou com `QTSUGESTAO = -2316`. Isso mostra
que a 3010 aceita sugestão negativa; não autoriza, sozinho, concluir toda a
fórmula.

## 3. Hipótese que o item 2.24 testa

Para cada item:

```text
base = QTGIRODIA × (PRAZOENTREGA + TEMREPOS)

se CONSIDERAESTPENDSUGCOMPRA = 'S':
    QTSUGESTAO = base × QTVEZES - ESTOQUE - QTPENDENTE

senão:
    QTSUGESTAO = base × QTVEZES - ESTOQUE
```

Para não chutar `QTVEZES`, o roteiro resolve a conta ao contrário:

```text
sem pendente: QTVEZES = (QTSUGESTAO + ESTOQUE) / base
com pendente: QTVEZES = (QTSUGESTAO + ESTOQUE + QTPENDENTE) / base
```

Ele agrupa os fatores inferidos com quatro casas **apenas para encontrar o grupo
mais comum**; ao recalcular a sugestão usa o valor real inferido, sem limitar a
quatro casas.

Os candidatos usados nesta primeira rodada são `PCFORNEC.PRAZOENTREGA` para o
prazo do fornecedor e `PCPRODUT.TEMREPOS` para o tempo de reposição. Isso é
hipótese operacional baseada no caminho já levantado e precisa ser confirmada
pelo resultado. Se a conta não fechar, uma das primeiras coisas a investigar é
se a 3010 usa algum prazo substituto/específico do item.

## 4. Como gerar o pedido de referência

Na base TESTE:

1. abrir a rotina 3010;
2. lançar manualmente um pedido de compra normal, pelo caminho que o time usa;
3. preferir **2 ou mais produtos**, para que um fator comum possa ser testado;
4. se possível, incluir produtos com `QTMINSUGCOMPRA` ou `MULTIPLOCOMPRAS`
   preenchidos, pois isso ajuda a revelar ajuste posterior à conta-base;
5. gravar o pedido e anotar o `NUMPED`;
6. rodar o item 2.24 logo em seguida, porque estoque, pendência e giro são dados
   vivos e podem mudar.

Não usar para essa evidência um pedido criado pela aplicação: precisamos observar
o resultado da **3010**, que é justamente a referência a reproduzir.

## 5. Como rodar

O `.env` deve continuar apontando para a base TESTE. O item é somente leitura e
usa as mesmas travas do restante do roteiro de homologação.

```bash
cd ~/ww/pedido-3010/api
NUMPED_QTSUGESTAO=<NUMPED> API_URL=nao npm run homologacao
```

`API_URL=nao` evita os testes HTTP e deixa esta rodada focada no banco. Não é
necessário ligar a API para o item 2.24.

Sem `NUMPED_QTSUGESTAO`, o 2.24 aparece como `pulado` e o restante do roteiro
continua funcionando como antes.

## 6. O que o 2.24 registra

Do pedido e de cada item:

```text
NUMPED e ROTINALANC
CODFILIAL e CODFORNEC
CODPROD
QTPEDIDA
QTSUGESTAO gravada pela 3010
ESTOQUE disponível atual
QTGIRODIA
QTPENDENTE
PCFILIAL.CONSIDERAESTPENDSUGCOMPRA
PCFORNEC.PRAZOENTREGA
PCPRODUT.TEMREPOS
QTMINSUGCOMPRA e MULTIPLOCOMPRAS do PCITEM e do cadastro atual
QTVEZES inferida sem e com pendente
QTVEZES escolhida conforme a regra da filial
QTVEZES mais comum entre os itens
valor recalculado pela conta-base e diferença para o gravado
```

O roteiro também recusa como referência um número cujo `ROTINALANC` não seja
`3010`.

## 7. Como interpretar o relatório

### Caso A — fecha limpo

Exemplo de saída esperada:

```text
QTVEZES inferida mais comum: 1 em 4/4 item(ns)
conta comum reproduz 4/4
```

Isso é evidência forte de que a conta-base e o tratamento de pendência estão
corretos para aquele cenário. Ainda assim, antes de codificar a regra de
produção, conferir os campos de mínimo/múltiplo e registrar a rodada.

### Caso B — a maioria fecha, alguns itens não

Olhar primeiro nos itens que destoaram:

- `QTMINSUGCOMPRA`;
- `MULTIPLOCOMPRAS`;
- diferença entre os valores gravados no `PCITEM` e os valores atuais do
  `PCPRODUT`;
- prazo/tempo de reposição aplicável ao item.

Se os divergentes forem justamente os que têm mínimo ou múltiplo, a próxima
etapa é descobrir a ordem e o arredondamento desse ajuste antes de mexer na
gravação da aplicação.

### Caso C — o fator muda de item para item

Não concluir que `QTVEZES` é variável por produto sem evidência adicional.
Primeiro conferir se o prazo usado pela 3010 é realmente
`PCFORNEC.PRAZOENTREGA + PCPRODUT.TEMREPOS` e se estoque/pendente não mudaram
entre a gravação e a execução do roteiro.

### Caso D — `QTGIRODIA = 0` ou dias-base = 0

Não há como inferir `QTVEZES` por divisão nesse item. Ele permanece no detalhe,
mas não deve ser usado para fechar o fator comum.

## 8. Critério para liberar a implementação

Não basta um único produto bater. Para trocar o `QTSUGESTAO = 0` provisório da
aplicação por um cálculo real, registrar pelo menos uma rodada com pedido criado
na 3010 e **vários itens**, e explicar qualquer divergência relevante —
principalmente quando houver mínimo ou múltiplo.

Depois disso:

1. registrar o relatório em `VALIDACAO_HOMOLOGACAO_RODADAS.md`;
2. criar teste de regressão com os valores reais observados;
3. implementar a regra na gravação;
4. repetir a conferência contra a 3010;
5. só então reconsiderar o gate de produção.
