# Validação — Time da importação com 3 LASTs da semana (25/09)

**Natureza:** observado em runtime na homologação (o time gravou pela aplicação)
+ decisões do time + correções cobertas por teste. **Reteste pendente** com o
código corrigido.

## 1. Os LASTs

```text
26MIW185F   -> gravado como 11861 (master 1052/0426)   3 itens, 2 produtos
26MOC267F   -> gravado como 11859 (master 1050/0426)   3 itens, 3 produtos
26MSR296F   -> gravado como 11860 (master 1051/0426)   6 itens, 6 produtos
```

Os três foram **apagados da TESTE** para o reteste (roteiro em
`06_OPERACAO/BASE_TESTE.md`). A linha "CNTR. NOS.:" dos LASTs (quantidade 1) é
a dos contêineres: o comex descarta, e não é item.

## 2. O que o time apontou

```text
avisos do comex que ficam      total FOB, nome da fábrica, porto de destino, data da invoice
avisos do comex que saem       número do contêiner, porto de embarque, cliente,
                               imagem com os dados bancários
erro 1  (26MSR296F)            peso líquido diferente do LAST
erro 2  (26MIW185F)            item repetido gravado em duas linhas; a 3010 mostra
                               duplicado sem validar; o certo é somar
pergunta                       LAST sem a soma dos valores: calcular pelos itens e avisar
```

## 3. Peso líquido: o que o banco mostrou

A regra de antes gravava o PESOLIQDI do **cadastro**. O LAST traz o N.W. de cada
linha; a conta **N.W. ÷ quantidade** reproduz o cadastro até a 6ª casa quando os
dois batem (26MZC289F: 490 kg ÷ 4.800 = 0,102083) e mostra onde ele está velho.

No 26MSR296F, **os 6 produtos** estavam com o cadastro diferente do LAST:

```text
código    produto   cadastro    LAST        diferença
BM19230   6839      0,85        0,91        +0,06
BM19231   6840      0,85        0,91        +0,06
BM19232   6841      1,6875      1,7125      +0,025
BM20201   7157      0,62        0,60        -0,02
BM20202   7158      0,62        0,60        -0,02
BM25060   11052     1,233333    1,283333    +0,05
```

O histórico desses produtos nos pedidos da 3010 (2019 a 2026) explica:

```text
6840, 6841, 7157, 7158   o peso muda de pedido para pedido (o 6841 passou por
                         1,66 / 1,7 / 1,6875 / 1,65 / 1,675): o time ajusta à mão
6839, 11052              sempre o mesmo (0,85 em 22 pedidos; 1,233333 em 3)
```

Mecânica (evidência do trace): o bloco da 3010 que roda depois de gravar faz
`PCPRODUT.PESOLIQDI = PCITEM.PESOLIQDI`. O cadastro guarda **o peso do último
pedido**, e só muda se alguém digitar outro na grade de itens da 3010.
**Conclusão:** não era erro de cadastro; a aplicação não fazia o ajuste que o
time faz à mão.

## 4. Item repetido

No 26MIW185F, o PJ10PCM veio nas linhas 11 e 12:

```text
linha 11   428 un   22,39 USD   9.582,92
linha 12   1.522 un 23,73 USD   36.117,06
soma       1.950 un 23,435887 USD (média ponderada)   45.699,98 = o total do LAST
```

## 5. Decisões do time (25/09)

```text
peso líquido da DI        N.W. da linha ÷ quantidade (6 casas); o cadastro só quando
                          o LAST não traz o peso da linha (com aviso)
item repetido             uma linha só; preços diferentes pela média ponderada
                          (o ajuste fino, se preciso, é feito na invoice; o
                          importante é não subir o mesmo item duas vezes)
aviso de peso             quando o peso do LAST difere mais de 10% do cadastro
avisos do comex           saem os 4 que o time não usa
total FOB                 a tela soma os itens e avisa quando falta a soma do LAST
```

## 6. Correções (cobertas por teste)

```text
0048 feat   prévia avisa o que não bloqueia (total FOB calculado, item repetido,
            linha sem peso) e traz o N.W. de cada linha
0049 fix    gravação soma o item repetido e grava o peso líquido do LAST
0050 feat   tela mostra os avisos (lista própria, separada das pendências)
0051 fix    aviso do total FOB quando falta a soma do LAST, mesmo com total na invoice
0052 feat   prévia dispensa os 4 avisos do comex; total FOB vazio não bloqueia
0053 feat   aviso quando o peso do LAST difere mais de 10% do cadastro
```

Antes do 0052, **os avisos do comex de nível "bloqueio" viravam pendência** e
impediam gravar; a imagem dos dados bancários é bloqueio para o comex (ele gera
a invoice).

## 7. Reteste (pendente)

Esperado com o código corrigido:

```text
26MIW185F   PJ10PCM numa linha só: 1.950 un a 23,435887, peso 4,765
26MSR296F   PESOLIQDI 0,91 / 0,91 / 1,7125 / 0,6 / 0,6 / 1,283333
PCPRODUT    o 6839 passa de 0,85 para 0,91 (o bloco da 3010 leva o peso do pedido)
tela        nenhum dos 4 avisos dispensados; nenhum aviso de peso (diferenças < 10%)
masters     a partir de 1050/0426
```
