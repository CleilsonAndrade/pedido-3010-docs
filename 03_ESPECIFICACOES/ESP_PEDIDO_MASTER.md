# ESP — Pedido Master de Importação na rotina 3010

Funcionalidade:            Pedido Master de Importação
Código:                    P3010
Versão do documento:       1.0
Comportamento homologado:  pedido-3010 @ b813ceb
Última demanda:            A VALIDAR — projeto anterior à adoção do padrão

**Estado desta ESP:** CANÔNICA — migração documental concluída em 2026-10-07.

Esta especificação consolida o comportamento funcional do Pedido Master 3010
a partir das regras sustentadas pelo repositório documental, código, testes,
traces e homologações existentes.

Os 85 critérios de aceite desta ESP estão reconciliados em
`04_VALIDACOES/MATRIZ_VALIDACAO.md`.

A conclusão da migração documental não significa homologação funcional integral:

- comportamento homologado permanece identificado como homologado;
- comportamento coberto apenas por testes continua identificado como testado;
- retestes e homologações pendentes permanecem explicitamente marcados;
- hipóteses continuam marcadas como hipótese ou `A VALIDAR`;
- documentos de arquitetura, fluxos, contratos e validações permanecem como
  fontes complementares de detalhe e evidência, sem competir com a ESP como
  referência funcional.

## Escopo funcional

A especificação cobre:

- autenticação e autorização;
- leitura e prévia dos LASTs;
- resolução de produtos;
- dados do pedido;
- tributação;
- cotação;
- cálculo;
- QTSUGESTAO;
- gravação do primeiro pedido do master.

## P3010-HU1 — Acessar o pedido-3010

O usuário do time de Importação deve acessar a aplicação usando suas
credenciais do WinThor, sem cadastro de senha próprio no pedido-3010.

### P3010-HU1-RN1 — Autenticação usa o usuário do WinThor

A aplicação deve autenticar o usuário pelo cadastro do WinThor e pela função
de validação de senha do próprio WinThor.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU1-RN1-CN1 — Usuário autorizado consegue entrar

Ação / entrada:
usuário e senha válidos do WinThor, pertencente ao setor exigido pela aplicação.

Resultado esperado:
a autenticação é aceita e uma sessão da aplicação é criada.

#### P3010-HU1-RN1-CN2 — Credencial inválida não permite acesso

Ação / entrada:
usuário inexistente ou senha inválida.

Resultado esperado:
a autenticação é recusada.

### P3010-HU1-RN2 — O acesso é restrito ao setor autorizado

O usuário autenticado precisa pertencer ao setor configurado para uso da
aplicação.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU1-RN2-CN1 — Usuário de outro setor é recusado

Ação / entrada:
credenciais válidas do WinThor, mas usuário fora do setor exigido.

Resultado esperado:
o acesso é recusado.

### P3010-HU1-RN3 — A filial usada na gravação precisa estar liberada ao usuário

A gravação só pode usar filial disponibilizada pela PCLIB para a matrícula do
usuário autenticado.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU1-RN3-CN1 — Filial sem permissão não pode ser gravada

Ação / entrada:
usuário autenticado solicita gravação em filial que não está liberada para sua
matrícula.

Resultado esperado:
a gravação é recusada antes de qualquer escrita no WinThor.

## P3010-HU2 — Conferir os LASTs antes do lançamento

O usuário do time de Importação deve conseguir enviar os LASTs para conferência
antes de qualquer gravação no WinThor.

### P3010-HU2-RN1 — A prévia é somente leitura

A prévia deve analisar os arquivos e devolver o que foi encontrado sem alterar
dados do WinThor.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU2-RN1-CN1 — Conferir LAST não grava no WinThor

Ação / entrada:
enviar um ou mais LASTs para a prévia.

Resultado esperado:
a aplicação devolve a conferência dos arquivos e nenhuma gravação é realizada
no WinThor.

### P3010-HU2-RN2 — Cada LAST representa um pedido

Cada planilha enviada deve ser tratada como um processo de pedido independente.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU2-RN2-CN1 — Vários LASTs geram conferências independentes

Ação / entrada:
enviar mais de um LAST na mesma prévia.

Resultado esperado:
cada arquivo possui seu próprio resultado de conferência e corresponde a um
pedido independente.

### P3010-HU2-RN3 — A leitura do LAST é responsabilidade do comex-api

O pedido-3010 não deve reimplementar a leitura das planilhas. Ele deve consumir
o resultado produzido pelo comex-api.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU2-RN3-CN1 — LAST legível retorna dados para conferência

Ação / entrada:
enviar um LAST que o comex-api consegue processar.

Resultado esperado:
os dados retornados pelo comex-api ficam disponíveis para as regras de
conferência do pedido-3010.

#### P3010-HU2-RN3-CN2 — Falha de leitura vira pendência

Ação / entrada:
enviar um LAST que o comex-api não consegue processar.

Resultado esperado:
o pedido correspondente recebe uma pendência de leitura e não fica liberado
para gravação.

### P3010-HU2-RN4 — O produto é resolvido pelo código de fábrica

A aplicação deve procurar produto ativo do WinThor pelo código de fábrica
informado no LAST.

A busca considera:

1. código igual após retirar espaços das pontas e comparar em maiúsculo;
2. forma normalizada sem hífen, `#` e espaço;
3. somente produtos com `DTEXCLUSAO IS NULL`.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU2-RN4-CN1 — Um único candidato resolve o produto

Ação / entrada:
o código de fábrica do LAST encontra exatamente um produto ativo.

Resultado esperado:
o produto é resolvido automaticamente para esse CODPROD.

#### P3010-HU2-RN4-CN2 — Nenhum candidato gera pendência

Ação / entrada:
o código de fábrica não encontra produto ativo.

Resultado esperado:
a prévia gera a pendência `PRODUTO_NAO_ENCONTRADO` e o pedido não fica
liberado para gravação.

#### P3010-HU2-RN4-CN3 — Mais de um candidato exige escolha

Ação / entrada:
o código de fábrica encontra mais de um produto ativo possível.

Resultado esperado:
a prévia gera `PRODUTO_AMBIGUO`, apresenta os candidatos e exige uma escolha
válida antes da gravação.

### P3010-HU2-RN5 — Divergência entre código e descrição exige decisão

Quando o código da linha e o início da descrição do LAST apontarem para
produtos diferentes, a aplicação não deve escolher silenciosamente um deles.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU2-RN5-CN1 — Código e descrição divergentes bloqueiam

Ação / entrada:
o código de fábrica aponta para um produto e a descrição aponta para outro.

Resultado esperado:
a prévia gera `CODIGO_DESCRICAO_DIVERGENTE`, apresenta as opções ao usuário e
o pedido permanece bloqueado até uma escolha válida.

### P3010-HU2-RN6 — Produto repetido no LAST vira uma única linha

Quando o mesmo produto aparecer em mais de uma linha do LAST, a aplicação deve
consolidar essas linhas antes da gravação.

A quantidade deve ser somada.

Quando os preços forem diferentes, o preço resultante deve ser a média
ponderada, preservando o valor total das linhas da invoice.

A prévia deve informar ao usuário que houve item repetido.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU2-RN6-CN1 — Produto repetido com mesmo preço é consolidado

Ação / entrada:
o mesmo produto aparece em duas ou mais linhas com o mesmo preço.

Resultado esperado:
a aplicação apresenta uma única linha para o produto, com a quantidade total
somada, e gera o aviso `ITEM_REPETIDO`.

#### P3010-HU2-RN6-CN2 — Produto repetido com preços diferentes usa média ponderada

Ação / entrada:
o mesmo produto aparece em duas ou mais linhas com preços diferentes.

Resultado esperado:
a aplicação apresenta uma única linha para o produto, soma as quantidades e
calcula o preço pela média ponderada, preservando o valor total das linhas,
além de gerar o aviso `ITEM_REPETIDO`.

### P3010-HU2-RN7 — O peso líquido do LAST tem prioridade sobre o cadastro

Quando o LAST informar o N.W. da linha, o peso líquido unitário usado pelo
pedido deve ser calculado por:

`N.W. da linha / quantidade`

O resultado deve ser tratado com 6 casas decimais.

O peso do cadastro é usado somente quando o LAST não fornecer o peso líquido.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU2-RN7-CN1 — Peso informado no LAST é usado no pedido

Ação / entrada:
a linha possui N.W. e quantidade válidos.

Resultado esperado:
o peso líquido unitário usado no pedido é o N.W. da linha dividido pela
quantidade.

#### P3010-HU2-RN7-CN2 — Ausência de peso no LAST usa o cadastro

Ação / entrada:
a linha não possui N.W., mas o produto possui peso disponível no cadastro.

Resultado esperado:
a aplicação usa o peso do cadastro e gera o aviso `SEM_PESO_NO_LAST`.

#### P3010-HU2-RN7-CN3 — Diferença superior a 10% gera aviso

Ação / entrada:
o peso calculado a partir do LAST difere mais de 10% do peso existente no
cadastro, para cima ou para baixo.

Resultado esperado:
a aplicação gera o aviso `PESO_DIFERENTE_DO_CADASTRO`, mas esse aviso não
bloqueia a gravação.

### P3010-HU2-RN8 — O pedido-3010 decide quais ocorrências do comex afetam a conferência

O `comex-api` continua responsável por identificar ocorrências da planilha.

O pedido-3010 decide quais dessas ocorrências são relevantes para o lançamento
do pedido master.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU2-RN8-CN1 — Ocorrência de bloqueio relevante impede a gravação

Ação / entrada:
o comex-api retorna uma ocorrência de nível `bloqueio` que não está entre as
ocorrências dispensadas pelo time de Importação.

Resultado esperado:
a prévia gera `BLOQUEIO_COMEX` e o pedido não fica liberado para gravação.

#### P3010-HU2-RN8-CN2 — Ocorrências dispensadas não bloqueiam o pedido

Ação / entrada:
o comex-api informa ausência de um dos seguintes dados:

- número do contêiner;
- porto de embarque;
- cliente;
- imagem dos dados bancários.

Resultado esperado:
essas ocorrências não geram pendência de gravação no pedido-3010.

#### P3010-HU2-RN8-CN3 — Total FOB ausente gera aviso, mas não bloqueia

Ação / entrada:
o LAST não traz o total FOB consolidado, mas os itens possuem valores que
permitem calcular o total.

Resultado esperado:
a aplicação calcula o total a partir dos itens, gera o aviso
`TOTAL_FOB_CALCULADO` e não bloqueia a gravação apenas por esse motivo.

### P3010-HU2-RN9 — Invoice já lançada exige confirmação, não bloqueio absoluto

A existência de pedido master do mesmo fornecedor com a mesma invoice deve ser
informada ao usuário.

A aplicação pode permitir continuar, mas a gravação exige motivo informado
pelo usuário.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU2-RN9-CN1 — Invoice sem master anterior segue normalmente

Ação / entrada:
não existe pedido master do mesmo fornecedor com a mesma invoice.

Resultado esperado:
a invoice repetida não gera pendência nem exige motivo.

#### P3010-HU2-RN9-CN2 — Invoice já usada exige motivo

Ação / entrada:
já existe pedido master do mesmo fornecedor com a mesma invoice.

Resultado esperado:
a aplicação informa os pedidos encontrados e exige um motivo antes de permitir
a gravação.

#### P3010-HU2-RN9-CN3 — Segundo pedido do mesmo master não é nova duplicidade

Ação / entrada:
a consulta encontra o primeiro e o segundo pedido pertencentes ao mesmo master.

Resultado esperado:
o conjunto deve ser tratado como um único lançamento da invoice, e não como duas
ocorrências independentes.

#### P3010-HU2-RN9-CN4 — Pedido cancelado continua aparecendo na conferência

Ação / entrada:
existe pedido com a mesma invoice, mas ele está cancelado.

Resultado esperado:
o pedido cancelado continua sendo apresentado na conferência da invoice já
lançada.

## P3010-HU3 — Preencher os dados do pedido

O usuário do time de Importação deve receber os dados iniciais conhecidos do
pedido já preenchidos quando os respectivos cadastros estiverem disponíveis,
mantendo a possibilidade de alterá-los.

### P3010-HU3-RN1 — A tela aplica defaults operacionais disponíveis

Os defaults operacionais são:

- filial `4`;
- comprador `201`;
- moeda `220`;
- incoterm `FOB`;
- via marítima;
- data da cotação igual à data corrente.

Um default somente pode ser aplicado quando o valor correspondente existir
entre as opções devolvidas pela API.

Demandas: legado — anterior à adoção deste padrão documental.

Status atual: IMPLEMENTADO e VALIDADO por testes automatizados.
Homologação funcional dos defaults operacionais: A VALIDAR.

#### P3010-HU3-RN1-CN1 — Filial 4 disponível inicia selecionada

Ação / entrada:
a lista de filiais permitidas ao usuário contém a filial `4`.

Resultado esperado:
a filial `4` inicia selecionada.

#### P3010-HU3-RN1-CN2 — Comprador 201 disponível inicia selecionado

Ação / entrada:
a lista de compradores contém o comprador `201`.

Resultado esperado:
o comprador `201` inicia selecionado.

#### P3010-HU3-RN1-CN3 — Default inexistente não é forçado

Ação / entrada:
um valor padrão não existe na respectiva lista devolvida pela API.

Resultado esperado:
a aplicação não usa um valor inexistente como seleção automática.

#### P3010-HU3-RN1-CN4 — Defaults continuam editáveis

Ação / entrada:
a tela iniciou com filial e comprador padrão preenchidos.

Resultado esperado:
o usuário pode alterar normalmente esses campos para outras opções permitidas.

### P3010-HU3-RN2 — O fornecedor do pedido vem do cadastro do WinThor

O nome existente no LAST serve como referência para localizar o fornecedor,
mas o pedido deve usar um fornecedor válido do cadastro do WinThor.

Fornecedor bloqueado não pode ser usado na gravação.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU3-RN2-CN1 — Fornecedor compatível pode ser selecionado

Ação / entrada:
o nome do fornecedor do LAST possui correspondência válida entre os
fornecedores retornados pelo WinThor.

Resultado esperado:
o fornecedor correspondente fica disponível para uso no pedido.

#### P3010-HU3-RN2-CN2 — Fornecedor bloqueado não pode ser usado

Ação / entrada:
o fornecedor localizado está bloqueado para o lançamento.

Resultado esperado:
o fornecedor não pode ser usado para gravar o pedido.

### P3010-HU3-RN3 — O país de origem vem do fornecedor selecionado

O país de origem do pedido deve acompanhar o cadastro do fornecedor escolhido
no WinThor.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU3-RN3-CN1 — Selecionar fornecedor define o país de origem

Ação / entrada:
o usuário seleciona um fornecedor válido que possui país cadastrado.

Resultado esperado:
o país de origem do pedido é preenchido com o país do fornecedor selecionado.

### P3010-HU3-RN4 — O porto de chegada pode ser sugerido pelo destino do LAST

Quando o destino informado no LAST permitir identificar de forma única um porto
disponível no WinThor, a aplicação deve usá-lo como valor inicial do porto de
chegada.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU3-RN4-CN1 — Destino com correspondência única preenche o porto

Ação / entrada:
o destino do LAST corresponde de forma única a um porto disponível no WinThor.

Resultado esperado:
o porto correspondente inicia selecionado como porto de chegada.

### P3010-HU3-RN5 — O porto de nacionalização acompanha o porto de chegada até edição manual

Enquanto o usuário não alterar manualmente o porto de nacionalização, ele deve
acompanhar o porto de chegada.

Depois da alteração manual, novas mudanças no porto de chegada não devem
sobrescrever o porto de nacionalização escolhido pelo usuário.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU3-RN5-CN1 — Porto de nacionalização acompanha a chegada inicialmente

Ação / entrada:
o porto de chegada é definido e o usuário ainda não alterou manualmente o porto
de nacionalização.

Resultado esperado:
o porto de nacionalização recebe o mesmo porto de chegada.

#### P3010-HU3-RN5-CN2 — Alteração manual da nacionalização é preservada

Ação / entrada:
o usuário altera manualmente o porto de nacionalização e depois modifica o porto
de chegada.

Resultado esperado:
o porto de nacionalização informado manualmente permanece inalterado.

#### P3010-HU3-RN5-CN3 — Tributação usa o porto de nacionalização

Ação / entrada:
porto de chegada e porto de nacionalização possuem valores diferentes.

Resultado esperado:
a consulta tributária do pedido usa o porto de nacionalização.

### P3010-HU3-RN6 — A proforma inicia com a invoice e permanece editável

O número da proforma deve iniciar com o número da invoice do LAST.

O usuário pode alterar esse valor quando a operação possuir uma proforma
diferente da invoice.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU3-RN6-CN1 — Invoice inicia a proforma

Ação / entrada:
o LAST possui número de invoice.

Resultado esperado:
o campo de proforma inicia com o mesmo número da invoice.

#### P3010-HU3-RN6-CN2 — Proforma pode ser alterada

Ação / entrada:
o usuário informa uma proforma diferente da invoice.

Resultado esperado:
o valor informado pelo usuário é mantido para o pedido.

### P3010-HU3-RN7 — As datas previstas possuem valores iniciais assistidos

Os valores iniciais são:

- previsão de embarque: data da invoice;
- previsão de chegada: preenchida pelo usuário;
- previsão de entrada no estoque: chegada + 20 dias.

A previsão de entrada acompanha a chegada + 20 dias enquanto o usuário ainda
não tiver alterado manualmente a entrada.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU3-RN7-CN1 — Embarque inicia com a data da invoice

Ação / entrada:
o LAST possui data da invoice.

Resultado esperado:
a previsão de embarque inicia com a data da invoice.

#### P3010-HU3-RN7-CN2 — Entrada é sugerida como chegada mais 20 dias

Ação / entrada:
o usuário informa a previsão de chegada e ainda não alterou manualmente a
previsão de entrada no estoque.

Resultado esperado:
a previsão de entrada no estoque é preenchida com a data de chegada mais
20 dias.

#### P3010-HU3-RN7-CN3 — Entrada alterada manualmente deixa de acompanhar a chegada

Ação / entrada:
o usuário altera manualmente a previsão de entrada no estoque e depois modifica
a previsão de chegada.

Resultado esperado:
a previsão de entrada informada manualmente é preservada.

### P3010-HU3-RN8 — As datas previstas devem respeitar a ordem cronológica

A ordem válida é:

`embarque <= chegada <= entrada no estoque`

Datas iguais são permitidas.

Demandas: legado — anterior à adoção deste padrão documental.

Status atual: IMPLEMENTADO e VALIDADO por testes automatizados.
Homologação pós-correção: A VALIDAR.

#### P3010-HU3-RN8-CN1 — Chegada anterior ao embarque é recusada

Ação / entrada:
a previsão de chegada é anterior à previsão de embarque.

Resultado esperado:
o pedido permanece bloqueado para gravação.

#### P3010-HU3-RN8-CN2 — Entrada anterior à chegada é recusada

Ação / entrada:
a previsão de entrada no estoque é anterior à previsão de chegada.

Resultado esperado:
o pedido permanece bloqueado para gravação.

#### P3010-HU3-RN8-CN3 — Datas iguais são permitidas

Ação / entrada:
embarque, chegada e entrada no estoque possuem a mesma data.

Resultado esperado:
a igualdade entre as datas não gera bloqueio cronológico.

## P3010-HU4 — Obter a cotação do pedido

O usuário deve receber a cotação aplicável ao pedido sem precisar calcular
manualmente o acréscimo operacional do dólar.

### P3010-HU4-RN1 — USD do dia usa BCB/PTAX com acréscimo de 5%

Quando a moeda for dólar americano (`220`) e a data da cotação for a data
corrente, a aplicação deve obter a cotação de venda do BCB/PTAX.

A cotação considerada pelo pedido é:

`cotacaoVenda + 5%`

equivalente a:

`cotacaoVenda × 1,05`

O resultado usado no WinThor deve respeitar 6 casas decimais.

Demandas: legado — anterior à adoção deste padrão documental.

Status atual: IMPLEMENTADO e VALIDADO por testes automatizados.
Homologação funcional da cotação BCB/PTAX com acréscimo de 5%: A VALIDAR.

#### P3010-HU4-RN1-CN1 — Cotação de venda recebe acréscimo de 5%

Ação / entrada:
o BCB retorna uma cotação de venda válida para USD na data corrente.

Resultado esperado:
a aplicação calcula a cotação considerada adicionando 5% à cotação de venda.

### P3010-HU4-RN2 — Fechamento PTAX tem preferência

Quando houver mais de um boletim no mesmo dia, a aplicação deve preferir o
`Fechamento PTAX`.

Se o fechamento ainda não estiver disponível, deve usar o boletim mais recente
do mesmo dia.

Demandas: legado — anterior à adoção deste padrão documental.

Status atual: IMPLEMENTADO e VALIDADO por testes automatizados.
Homologação funcional da seleção do boletim PTAX: A VALIDAR.

#### P3010-HU4-RN2-CN1 — Fechamento disponível é escolhido

Ação / entrada:
o BCB retorna vários boletins do dia, incluindo `Fechamento PTAX`.

Resultado esperado:
a cotação considerada usa o boletim `Fechamento PTAX`.

#### P3010-HU4-RN2-CN2 — Sem fechamento usa o boletim mais recente do dia

Ação / entrada:
o BCB retorna boletins do dia, mas ainda não existe `Fechamento PTAX`.

Resultado esperado:
a aplicação usa o boletim mais recente disponível naquela mesma data.

#### P3010-HU4-RN2-CN3 — Não há fallback automático para outro dia

Ação / entrada:
não existe boletim disponível para a data solicitada.

Resultado esperado:
a aplicação não substitui silenciosamente a cotação pela de outro dia.

### P3010-HU4-RN3 — A cotação USD do dia pode ser cadastrada automaticamente no WinThor

Para USD na data corrente, a cotação considerada pelo pedido pode ser gravada
automaticamente em `PCCOTACAOMOEDAI`.

Essa escrita depende da chave:

`COTACAO_BCB_GRAVACAO_ATIVA=S`

A chave de cotação é independente da chave de gravação do pedido:

`GRAVACAO_3010_ATIVA`

Demandas: legado — anterior à adoção deste padrão documental.

Status atual: IMPLEMENTADO e VALIDADO por testes automatizados.
Proteção com `COTACAO_BCB_GRAVACAO_ATIVA` desligada: VALIDADA por teste
automatizado, sem tentativa de escrita no Oracle.
Gravação automática com a chave ligada: VALIDADA por testes automatizados da
orquestração e da persistência Oracle.
Homologação funcional da gravação automática na base TESTE: A VALIDAR.

#### P3010-HU4-RN3-CN1 — Chave ligada permite atualizar a cotação do dia

Ação / entrada:
moeda `220`, data corrente, cotação BCB disponível e
`COTACAO_BCB_GRAVACAO_ATIVA=S`.

Resultado esperado:
a cotação considerada é cadastrada no WinThor para a moeda e a data solicitadas.

#### P3010-HU4-RN3-CN2 — Chave desligada impede a escrita automática

Ação / entrada:
é solicitada a atualização automática da cotação com
`COTACAO_BCB_GRAVACAO_ATIVA` desligada.

Resultado esperado:
a aplicação não altera `PCCOTACAOMOEDAI`.

### P3010-HU4-RN4 — Cotação histórica não é sobrescrita automaticamente pelo BCB

A atualização automática pelo BCB aplica-se ao USD da data corrente.

Para data histórica, a aplicação deve usar a cotação já cadastrada no WinThor,
sem substituí-la automaticamente por uma consulta ao BCB.

Demandas: legado — anterior à adoção deste padrão documental.

Status atual: IMPLEMENTADO e VALIDADO por testes automatizados.
Homologação funcional da preservação de cotações históricas: A VALIDAR.

#### P3010-HU4-RN4-CN1 — Data histórica preserva a cotação cadastrada

Ação / entrada:
o pedido usa USD com data de cotação anterior à data corrente.

Resultado esperado:
a aplicação consulta a cotação já cadastrada no WinThor e não executa
atualização automática dessa data pelo BCB.

### P3010-HU4-RN5 — Falha na cotação BCB do dia não reutiliza valor antigo

Para USD na data corrente, a aplicação não deve tratar uma cotação antiga já
existente no WinThor como se fosse a cotação atual quando a consulta ou a
atualização pelo BCB falhar.

Demandas: legado — anterior à adoção deste padrão documental.

Status atual: IMPLEMENTADO e VALIDADO por testes automatizados.
Homologação funcional do bloqueio por falha na cotação BCB do dia: A VALIDAR.

#### P3010-HU4-RN5-CN1 — Falha do BCB mantém o pedido sem cotação válida

Ação / entrada:
moeda `220`, data corrente e falha ao obter ou cadastrar a cotação pelo
BCB/PTAX.

Resultado esperado:
a aplicação mantém a cotação atual como indisponível para o pedido e não
reutiliza silenciosamente uma cotação anterior.

#### P3010-HU4-RN5-CN2 — Pedido sem cotação atual não pode ser gravado

Ação / entrada:
a atualização da cotação USD da data corrente falhou.

Resultado esperado:
o pedido permanece bloqueado para gravação até existir uma cotação válida para
a data corrente.

### P3010-HU4-RN6 — A cotação USD do dia é sincronizada novamente antes da gravação

Mesmo que a tela já tenha obtido e cadastrado a cotação, o backend deve
sincronizar novamente a cotação USD da data corrente imediatamente antes de
montar e gravar o pedido.

A cotação usada no pedido deve ser o valor confirmado nessa sincronização.

Demandas: legado — anterior à adoção deste padrão documental.

Status atual: IMPLEMENTADO e VALIDADO por testes automatizados.
Homologação funcional da ressincronização imediatamente antes da gravação:
A VALIDAR.

#### P3010-HU4-RN6-CN1 — Gravação usa a cotação confirmada na sincronização final

Ação / entrada:
pedido em USD com data de cotação igual à data corrente e sincronização BCB
concluída com sucesso.

Resultado esperado:
o pedido usa a cotação confirmada pela sincronização executada imediatamente
antes da gravação.

#### P3010-HU4-RN6-CN2 — Falha na sincronização final impede o pedido

Ação / entrada:
a sincronização BCB/PTAX imediatamente anterior à gravação falha.

Resultado esperado:
o pedido não é gravado no WinThor.

### P3010-HU4-RN7 — Atualizações concorrentes da mesma cotação são serializadas

Dentro da mesma instância da API, operações simultâneas para a mesma combinação
de moeda e data não devem executar a atualização da cotação em paralelo.

A operação seguinte deve aguardar a anterior terminar antes de iniciar sua
própria sincronização.

Demandas: legado — anterior à adoção deste padrão documental.

Status atual: IMPLEMENTADO e VALIDADO por teste automatizado.
Homologação funcional da serialização concorrente: A VALIDAR.

#### P3010-HU4-RN7-CN1 — Segunda atualização aguarda a primeira

Ação / entrada:
duas solicitações de atualização da mesma moeda e data são iniciadas
praticamente ao mesmo tempo na mesma instância da API.

Resultado esperado:
a segunda solicitação aguarda o término da primeira antes de executar sua
sincronização com BCB e WinThor.

#### P3010-HU4-RN7-CN2 — Moeda ou data diferente não compartilha a mesma fila

Ação / entrada:
existem solicitações simultâneas para combinações diferentes de moeda e data.

Resultado esperado:
uma combinação não precisa aguardar a fila de outra combinação distinta.

### Limitação conhecida de P3010-HU4-RN7

A serialização atual existe somente dentro de uma instância da API.

Se a aplicação passar a operar com múltiplas instâncias simultâneas, será
necessário validar e definir um mecanismo de coordenação compartilhada ou
proteção equivalente no Oracle.

## P3010-HU5 — Determinar a tributação dos itens

Cada produto do pedido deve possuir uma tributação válida para o contexto da
importação antes da gravação no WinThor.

### P3010-HU5-RN1 — A tributação é obtida do WinThor pelo contexto do pedido

A aplicação deve consultar a tributação do item considerando, no mínimo:

- filial;
- fornecedor;
- país de origem;
- porto de nacionalização;
- produto.

A tributação utilizada na gravação deve ser novamente determinada pelo backend,
sem depender apenas dos valores apresentados anteriormente na tela.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU5-RN1-CN1 — Contexto válido retorna tributação utilizável

Ação / entrada:
produto e contexto do pedido possuem tributação aplicável no WinThor.

Resultado esperado:
a aplicação obtém a tributação correspondente e o item pode seguir para as
demais validações do pedido.

#### P3010-HU5-RN1-CN2 — Item sem tributação utilizável não pode ser gravado

Ação / entrada:
o WinThor não fornece uma tributação utilizável para o produto no contexto do
pedido.

Resultado esperado:
o item permanece com pendência e o pedido não é liberado para gravação enquanto
a tributação não estiver resolvida.

### P3010-HU5-RN2 — PIS e COFINS consideram exceções do WinThor

A determinação de PIS e COFINS deve considerar as exceções aplicáveis ao item
cadastradas no WinThor.

Quando existir uma exceção aplicável, a tributação utilizada pelo pedido deve
refletir essa exceção em vez de ignorá-la e usar somente os percentuais gerais.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU5-RN2-CN1 — Exceção aplicável é considerada

Ação / entrada:
o produto possui uma exceção de PIS e/ou COFINS aplicável ao contexto do pedido
no WinThor.

Resultado esperado:
os percentuais tributários usados para o item refletem a exceção aplicável.

#### P3010-HU5-RN2-CN2 — Ausência de exceção segue a tributação normal

Ação / entrada:
não existe exceção de PIS ou COFINS aplicável ao item no contexto do pedido.

Resultado esperado:
a aplicação utiliza a tributação normal determinada pelo WinThor para o item.

### P3010-HU5-RN3 — II e IPI seguem a tributação determinada pelo WinThor

Os percentuais de Imposto de Importação (II) e IPI usados no pedido devem ser
os percentuais determinados pelo WinThor para o produto e o contexto da
importação.

A gravação deve usar os percentuais revalidados pelo backend no momento do
processamento do pedido.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU5-RN3-CN1 — II aplicável é usado no item

Ação / entrada:
o WinThor determina percentual de Imposto de Importação para o produto no
contexto do pedido.

Resultado esperado:
o item usa esse percentual de II na tributação considerada para a gravação.

#### P3010-HU5-RN3-CN2 — IPI aplicável é usado no item

Ação / entrada:
o WinThor determina percentual de IPI para o produto no contexto do pedido.

Resultado esperado:
o item usa esse percentual de IPI na tributação considerada para a gravação.

## P3010-HU6 — Calcular os valores do pedido

O usuário deve receber os valores calculados do pedido conforme as regras
observadas na rotina 3010 antes da gravação no WinThor.

### P3010-HU6-RN1 — O cálculo usa os dados consolidados do item e do pedido

O cálculo deve considerar os dados já resolvidos e validados nas etapas
anteriores, incluindo:

- produto;
- quantidade;
- preço de compra;
- percentuais tributários aplicáveis;
- cotação da moeda;
- totais necessários ao cálculo do pedido.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU6-RN1-CN1 — Item válido pode ser calculado

Ação / entrada:
o item possui produto resolvido, quantidade, preço de compra, tributação e
cotação válidos.

Resultado esperado:
a aplicação calcula os valores derivados necessários para o item e para o
pedido.

#### P3010-HU6-RN1-CN2 — Dado obrigatório ausente impede concluir o cálculo

Ação / entrada:
falta um dado obrigatório necessário para calcular corretamente o item.

Resultado esperado:
o cálculo não é considerado concluído e o pedido não fica liberado para
gravação enquanto a pendência permanecer.

### P3010-HU6-RN2 — Os valores derivados do item devem reproduzir a rotina 3010

Para o escopo de cálculo já homologado, os valores derivados de cada item devem
reproduzir o comportamento observado na rotina 3010.

A comparação dos valores decimais deve preservar a precisão necessária até a
6ª casa decimal nos campos calculados por item.

Demandas: legado — anterior à adoção deste padrão documental.

Status atual: HOMOLOGADO no escopo atualmente validado do primeiro pedido.

#### P3010-HU6-RN2-CN1 — Item calculado reproduz os valores da rotina 3010

Ação / entrada:
um item é processado com os mesmos dados de produto, quantidade, preço,
tributação, cotação e demais valores necessários usados pela rotina 3010.

Resultado esperado:
os valores derivados do item correspondem aos valores produzidos pela rotina
3010 dentro da precisão definida para o cálculo.

#### P3010-HU6-RN2-CN2 — Divergência de cálculo impede considerar o pedido validado

Ação / entrada:
um valor derivado do item diverge do comportamento esperado da rotina 3010
fora da precisão aceita.

Resultado esperado:
o cálculo é considerado divergente e não deve ser tratado como validado para
gravação até a causa ser resolvida.

### P3010-HU6-RN3 — O total do pedido deve reproduzir a rotina 3010

O valor total calculado para o pedido deve reproduzir o comportamento da rotina
3010 dentro do escopo já homologado.

Demandas: legado — anterior à adoção deste padrão documental.

Status atual:
HOMOLOGADO para o primeiro pedido no escopo atualmente validado.

Na comparação histórica da homologação, o `VLTOTAL` apresentou diferença
residual de até R$ 0,02 em relação à rotina 3010.

Essa diferença observada não constitui, por si só, uma tolerância funcional
autorizada para novos cálculos.

#### P3010-HU6-RN3-CN1 — Total do primeiro pedido é calculado

Ação / entrada:
todos os itens do primeiro pedido possuem os dados necessários para o cálculo.

Resultado esperado:
a aplicação produz o valor total do pedido segundo as regras de cálculo
homologadas para esse escopo.

#### P3010-HU6-RN3-CN2 — Divergência do total deve ser identificada

Ação / entrada:
o total calculado pela aplicação diverge do valor esperado segundo o
comportamento homologado da rotina 3010.

Resultado esperado:
a divergência deve ser identificada na validação e não pode ser ocultada por
arredondamento ou ajuste sem regra comprovada.

### Limitação conhecida de P3010-HU6-RN3

O comportamento de `VLTOTAL` em cenários com frete e despesas que não pertencem
ao escopo atualmente fechado permanece A VALIDAR.

Nenhuma fórmula adicional para esse cenário deve ser tratada como regra
homologada até existir evidência suficiente.

### P3010-HU6-RN4 — A QTSUGESTAO reproduz a conta-base homologada da 3010

Para filial que não considera estoque pendente na sugestão de compra, a
quantidade sugerida deve ser calculada por:

`QTSUGESTAO = QTGIRODIA × (PRAZOENTREGA + TEMREPOS) - ESTOQUE_DISPONIVEL`

A conta-base não utiliza `QTVEZES`.

O resultado negativo deve ser preservado.

Demandas: legado — anterior à adoção deste padrão documental.

Status atual:
HOMOLOGADO para filial com `CONSIDERAESTPENDSUGCOMPRA='N'`.

#### P3010-HU6-RN4-CN1 — Conta-base calcula a quantidade sugerida

Ação / entrada:
a filial não considera estoque pendente e o item possui giro diário, prazo de
entrega, tempo de reposição e estoque disponível válidos.

Resultado esperado:
a aplicação calcula `QTSUGESTAO` pela conta-base homologada.

#### P3010-HU6-RN4-CN2 — Resultado negativo é preservado

Ação / entrada:
a conta-base resulta em uma `QTSUGESTAO` menor que zero.

Resultado esperado:
o valor negativo é preservado, sem ser convertido automaticamente para zero.

#### P3010-HU6-RN4-CN3 — QTVEZES não altera a conta-base homologada

Ação / entrada:
existe valor de `QTVEZES` associado ao cenário calculado.

Resultado esperado:
`QTVEZES` não participa da conta-base homologada da `QTSUGESTAO`.

### Limitação conhecida de P3010-HU6-RN4

O cálculo para filial com `CONSIDERAESTPENDSUGCOMPRA='S'` permanece
NÃO HOMOLOGADO.

Enquanto esse comportamento não for comprovado, a aplicação deve recusar a
gravação nesse cenário em vez de aplicar uma fórmula presumida.

## P3010-HU7 — Gravar o primeiro pedido no WinThor

Depois que a conferência, a tributação e o cálculo estiverem válidos, a
aplicação deve conseguir gravar o primeiro pedido do master no WinThor.

Status atual:
HOMOLOGADO na base TESTE para o primeiro pedido.
Publicação em produção: NÃO REALIZADA.

### P3010-HU7-RN1 — A gravação do pedido depende de habilitação explícita

A escrita do pedido no WinThor somente pode ser executada quando:

`GRAVACAO_3010_ATIVA=S`

Com a gravação desabilitada, a aplicação não deve criar ou alterar registros do
pedido no WinThor.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU7-RN1-CN1 — Chave desligada impede a gravação

Ação / entrada:
o usuário solicita a gravação com `GRAVACAO_3010_ATIVA` desligada.

Resultado esperado:
nenhum pedido é criado no WinThor.

#### P3010-HU7-RN1-CN2 — Chave ligada permite seguir para as validações de gravação

Ação / entrada:
o usuário solicita a gravação com `GRAVACAO_3010_ATIVA=S`.

Resultado esperado:
a aplicação pode prosseguir para as validações obrigatórias anteriores à escrita
do pedido.

### P3010-HU7-RN2 — O backend revalida o pedido antes de qualquer escrita

A gravação não deve confiar somente na conferência já realizada na tela.

Imediatamente antes da escrita, o backend deve revalidar os dados necessários
ao pedido, incluindo:

- integridade do LAST usado na operação;
- escolhas feitas para produtos com pendência de resolução;
- cadastros obrigatórios do pedido;
- filial permitida ao usuário;
- fornecedor;
- comprador;
- moeda e cotação aplicável;
- país e portos;
- tributação dos produtos;
- negociação;
- situação de invoice já lançada;
- regras de cálculo necessárias para a gravação.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU7-RN2-CN1 — Pedido ainda válido pode seguir para escrita

Ação / entrada:
todos os dados e regras revalidados pelo backend continuam válidos no momento da
solicitação de gravação.

Resultado esperado:
a aplicação pode seguir para a etapa transacional de escrita no WinThor.

#### P3010-HU7-RN2-CN2 — Mudança ou inconsistência bloqueia antes da escrita

Ação / entrada:
algum dado necessário não corresponde mais ao estado válido esperado no momento
da revalidação.

Resultado esperado:
a gravação é recusada antes da criação do pedido no WinThor.

### P3010-HU7-RN3 — A gravação do pedido é atômica

As escritas necessárias para criar o primeiro pedido devem ocorrer dentro da
mesma transação Oracle.

O pedido somente deve ser confirmado quando todas as etapas obrigatórias da
gravação forem concluídas com sucesso.

Se qualquer etapa falhar, a transação deve ser desfeita para não deixar um
pedido parcialmente gravado.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU7-RN3-CN1 — Gravação completa confirma a transação

Ação / entrada:
todas as escritas e processamentos obrigatórios do primeiro pedido são
concluídos com sucesso.

Resultado esperado:
a transação é confirmada e o pedido fica persistido integralmente no WinThor.

#### P3010-HU7-RN3-CN2 — Falha durante a escrita desfaz a transação

Ação / entrada:
ocorre erro depois do início da transação e antes da conclusão da gravação.

Resultado esperado:
a transação é desfeita e o pedido não permanece parcialmente gravado no
WinThor.

### P3010-HU7-RN4 — O IDPEDIDOMASTER não pode reutilizar um master existente

O `IDPEDIDOMASTER` do primeiro pedido deve ser obtido a partir do numerador de
importação do WinThor (`PCNUMERADORIMP`).

Antes de usar o próximo número, a aplicação deve garantir que ele não reutiliza
um master já existente no período correspondente.

Um pedido existente nunca deve ser apagado ou sobrescrito para liberar um
identificador de master.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU7-RN4-CN1 — Próximo numerador livre pode ser usado

Ação / entrada:
o próximo número disponível no numerador de importação é maior que os masters já
utilizados no período correspondente.

Resultado esperado:
a aplicação pode gerar um novo `IDPEDIDOMASTER` para o primeiro pedido.

#### P3010-HU7-RN4-CN2 — Numerador que causaria colisão não pode ser usado

Ação / entrada:
o próximo número do numerador resultaria em um `IDPEDIDOMASTER` já existente.

Resultado esperado:
a aplicação não grava o pedido usando esse identificador conflitante.

#### P3010-HU7-RN4-CN3 — Master existente não é removido para permitir nova gravação

Ação / entrada:
existe conflito entre o identificador que seria gerado e um master já gravado.

Resultado esperado:
o registro existente é preservado e a nova gravação não reutiliza esse
identificador.

### P3010-HU7-RN5 — O primeiro pedido grava cabeçalho e todos os itens válidos

A gravação do primeiro pedido deve persistir o cabeçalho do pedido e todos os
itens válidos pertencentes ao LAST processado.

Os dados gravados devem refletir o contexto já validado nas etapas anteriores,
sem depender de nova edição durante a escrita.

Todos os itens do pedido devem permanecer vinculados ao mesmo pedido e ao mesmo
master gerado para a operação.

Demandas: legado — anterior à adoção deste padrão documental.

Status atual:
HOMOLOGADO na base TESTE para o primeiro pedido.

#### P3010-HU7-RN5-CN1 — Cabeçalho é persistido com os dados validados

Ação / entrada:
o pedido passa por todas as validações obrigatórias e entra na etapa de
gravação.

Resultado esperado:
o cabeçalho do primeiro pedido é persistido com os dados validados da operação.

#### P3010-HU7-RN5-CN2 — Todos os itens válidos são persistidos

Ação / entrada:
o LAST possui um ou mais itens válidos após resolução, tributação e cálculo.

Resultado esperado:
todos os itens válidos são gravados vinculados ao primeiro pedido.

#### P3010-HU7-RN5-CN3 — Nenhum item válido pode ser omitido silenciosamente

Ação / entrada:
um item esperado não pode ser persistido durante a gravação.

Resultado esperado:
a gravação não é considerada concluída e deve seguir a regra de atomicidade da
P3010-HU7-RN3.

### P3010-HU7-RN6 — Os processamentos obrigatórios devem terminar antes do commit

Depois da inserção do cabeçalho e dos itens, a aplicação deve executar os
processamentos obrigatórios necessários para concluir a gravação do primeiro
pedido.

Esses processamentos fazem parte da mesma operação transacional e devem terminar
com sucesso antes da confirmação definitiva da gravação.

Demandas: legado — anterior à adoção deste padrão documental.

#### P3010-HU7-RN6-CN1 — Processamentos concluídos permitem confirmar o pedido

Ação / entrada:
o cabeçalho e os itens foram inseridos e todos os processamentos obrigatórios
posteriores foram concluídos com sucesso.

Resultado esperado:
a aplicação pode confirmar a transação e considerar o primeiro pedido gravado.

#### P3010-HU7-RN6-CN2 — Falha em processamento posterior impede o commit

Ação / entrada:
um processamento obrigatório falha depois da inserção do cabeçalho ou dos
itens.

Resultado esperado:
a gravação não é confirmada e deve seguir a regra de atomicidade da
P3010-HU7-RN3.

## Itens removidos

Nenhum item removido até o momento.
