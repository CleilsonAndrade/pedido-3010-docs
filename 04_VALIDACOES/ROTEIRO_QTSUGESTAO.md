# Validação — QTSUGESTAO da rotina 3010

**Natureza:** validação concluída para o caminho homologado
**Data de referência:** 2026-09-30
**Código implementado:** `b813ceb feat: calcula QTSUGESTAO como a rotina 3010`
**Correção de apoio:** `c96e389 fix: usa PCEST na validacao da QTSUGESTAO`
**Caso nativo de referência:** pedido 11866, filial 4, fornecedor 15

---

## 1. Objetivo

Confirmar com um pedido lançado manualmente pela própria 3010, na base TESTE, a
conta usada para gravar `PCITEM.QTSUGESTAO` e implementar somente o caminho
comprovado por evidência.

A investigação começou no patch 0055. A hipótese inicial incluía `QTVEZES`, mas
os testes manuais na própria 3010 mostraram que esse fator não participa da
conta-base observada neste caminho.

## 2. Regra homologada

Para filial que **não considera estoque pendente na sugestão de compra**:

```text
ESTOQUE_IDEAL =
    QTGIRODIA × (PRAZOENTREGA + TEMREPOS)

QTSUGESTAO =
    ESTOQUE_IDEAL - ESTOQUE_DISPONIVEL
```

Fontes usadas pela implementação:

```text
QTGIRODIA            PCEST.QTGIRODIA
PRAZOENTREGA         PCFORNEC.PRAZOENTREGA
TEMREPOS             PCPRODUT.TEMREPOS
ESTOQUE_DISPONIVEL   PKG_ESTOQUE.ESTOQUE_DISPONIVEL(CODPROD, CODFILIAL, 'C')
```

O resultado negativo é preservado.

## 3. Pedido nativo usado como referência

Pedido criado pela própria rotina 3010:

```text
NUMPED              11866
CODFILIAL           4
CODFORNEC           15
ROTINALANC          3010
CONSIDERAESTPENDSUGCOMPRA = N
```

Itens:

```text
produto 8360
QTGIRODIA           1
PRAZOENTREGA        150
TEMREPOS            21
ESTOQUE             925
QTPENDENTE          6
QTSUGESTAO gravada  -754

1 × (150 + 21) - 925 = -754
```

```text
produto 11190
QTGIRODIA           10
PRAZOENTREGA        150
TEMREPOS            21
ESTOQUE             0
QTPENDENTE          881
QTSUGESTAO gravada  1710

10 × (150 + 21) - 0 = 1710
```

O item 2.24 reproduziu **2 de 2 itens**, ambos com diferença zero.

## 4. Testes manuais na PCSIS3010

Além do pedido 11866, foram feitos testes diretos na
**PCSIS3010 v37.0.08.071**, antes de gravar o pedido.

### 4.1 QTVEZES

Com produto 8360:

```text
Qt. vezes estq. ideal = 2
PRAZOENTREGA          = 150
TEMREPOS              = 21
ESTOQUE               = 925

Qtde Est. Ideal       = 171
Qtde Sugestão         = -754
```

Portanto, alterar `QTVEZES` de 1 para 2 **não alterou** o estoque ideal nem a
`QTSUGESTAO` nesse caminho.

`QTVEZES` não entra na conta-base homologada.

### 4.2 Tempo de reposição informado na tela

Com `Tempo reposição = 10`:

```text
1 × (150 + 10) - 925 = -765
```

Isso confirmou que, quando há valor positivo informado na tela, ele substitui o
tempo de reposição do cadastro.

Com o campo em zero, o caminho observado usa `PCPRODUT.TEMREPOS`.

### 4.3 Prazo de entrega informado na tela

Com `Prazo entrega = 20`:

```text
1 × (20 + 21) - 925 = -884
```

Isso confirmou que, quando há valor positivo informado na tela, ele substitui o
prazo padrão.

Com o campo em zero, o caminho observado usa o prazo do fornecedor, que no caso
homologado corresponde a `PCFORNEC.PRAZOENTREGA`.

A aplicação atual não expõe esses dois campos de sobrescrita; portanto usa os
valores de cadastro.

## 5. Estoque pendente

A filial 4 usada na homologação possui:

```text
CONSIDERAESTPENDSUGCOMPRA = N
```

Também foi consultada a base TESTE e não foi encontrada filial com:

```text
CONSIDERAESTPENDSUGCOMPRA = S
```

Por isso **não existe evidência suficiente** para implementar o ramo que
considera estoque pendente.

A aplicação adota comportamento seguro:

```text
se CONSIDERAESTPENDSUGCOMPRA = 'S'
    recusar a gravação
    informar que esse cálculo ainda não foi homologado
```

Não subtrair `QTPENDENTE` por hipótese.

## 6. Mínimo e múltiplo de compra

O trace lê:

```text
QTMINSUGCOMPRA
MULTIPLOCOMPRAS
```

Mas não foi encontrado caso positivo útil para homologação:

```text
PCPRODUT / PCPRODFILIAL na filial 4     nenhum caso positivo relevante
histórico PCITEM da rotina 3010 filial 4 nenhum caso positivo relevante
```

Por isso esses campos permanecem apenas como diagnóstico.

Nenhum ajuste por mínimo ou múltiplo foi implementado sem evidência.

## 7. Item 2.24 do roteiro de homologação

Executar:

```bash
cd ~/ww/pedido-3010/api
NUMPED_QTSUGESTAO=<NUMPED> API_URL=nao npm run homologacao
```

O item:

- exige pedido com `ROTINALANC = 3010`;
- lê a `QTSUGESTAO` gravada;
- lê giro, estoque, prazo, reposição, pendência, mínimo e múltiplo;
- calcula a conta-base homologada;
- mostra a diferença entre calculado e gravado;
- registra se cada item reproduziu a 3010.

Para o pedido 11866:

```text
pedido 11866 · 2 item(ns) · pendente não considerado ·
conta-base reproduz 2/2
```

## 8. Implementação

A gravação deixou de usar `QTSUGESTAO = 0`.

Código:

```text
c96e389  fix: usa PCEST na validacao da QTSUGESTAO
b813ceb  feat: calcula QTSUGESTAO como a rotina 3010
```

A conta foi isolada em função própria e coberta por testes com os casos reais e
os testes manuais:

```text
11190  -> 1710
8360   -> -754
tempo reposição 10 -> -765
prazo entrega 20   -> -884
```

A gravação também recusa filial com estoque pendente enquanto esse ramo não for
homologado.

## 9. Validação final

Antes do commit:

```text
testes focados    96 / 96 PASS
suite completa    330 / 330 PASS
build             PASS
```

Homologação final depois do commit `b813ceb`, em transação somente leitura:

```text
16 ok · 5 diferente · 0 erro · 17 info · 2 pulado
```

Item 2.24:

```text
pedido 11866 · 2 item(ns) · pendente não considerado ·
conta-base reproduz 2/2
```

## 10. Limite atual

A regra está fechada para o caminho observado e implementado.

Continua em aberto somente o comportamento de `QTSUGESTAO` para uma filial com:

```text
CONSIDERAESTPENDSUGCOMPRA = 'S'
```

Esse cenário deve ser homologado antes de ser habilitado.
