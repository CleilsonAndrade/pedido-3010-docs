# Fluxo — Tela de conferência (Angular, pasta `web/`)

A tela do time de importação (setor 18). Aplicação **separada da API**, com
publicação própria (ainda não publicada). Coberta por 69 testes (Vitest + jsdom,
sem navegador).

## 1. Caminho do usuário

```text
entrar (usuário e senha do WinThor)
   |
   v
soltar os LASTs (.xls/.xlsx, até 60)  ->  POST /api/v1/previa
   |
   v
um bloco por pedido:
   cabeçalho do LAST (fornecedor, data, embarque e destino, contêiner, total FOB)
   O que falta resolver     pendências, na faixa amarela e preta
   Avisos                   o que não bloqueia (lista própria, sem a faixa)
   Invoice já lançada       os pedidos da 3010 agrupados por master (1º e 2º)
   Escolhas desta conferência
   Dados do pedido na 3010  (seção 2)
   Itens do LAST            produto do WinThor, com a descrição do LAST embaixo;
                            linha trocada ou ambígua mostra as opções para marcar
   Gravar na 3010           (seção 3)
```

## 2. Dados do pedido

```text
fornecedor      buscado pelo nome da planilha (sem "CO., LTD"); marcado sozinho só
                com nome IDÊNTICO; bloqueado aparece mas não pode ser escolhido
filial          PCLIB do usuário (marcada se ele só tem uma); não é lembrada
comprador       escolhido a cada pedido; não é lembrado
moeda           220 (a do trace)
data/cotação    hoje, com a cotação do WinThor para a moeda e a data
incoterm, via   FOB, marítima
país            do fornecedor
portos          chegada pelo destino do LAST; nacionalização (o dos impostos)
                acompanha a chegada até alguém mudar
negociação      sugestão da API (maior da 3010 no ano + 1) e quem usou a última;
                regra A enquanto digita (bloqueio vira pendência, aviso junto do campo)
proforma        = invoice, editável
datas           embarque = data da invoice; chegada DIGITADA; entrada = chegada + 20
                (acompanha até alguém mudar)
motivo          obrigatório quando o fornecedor já tem master desta invoice (decisão D)
```

## 3. Gravar na 3010

```text
botão liga só com: bloco sem pendência + gravação ligada + o LAST guardado + SHA-256
"Gravar na 3010" -> "Isso cria o pedido no WinThor" -> Confirmar e gravar -> Gravando...
   201   "Gravado na 3010: pedido 11858, master 1049/0426."  (o botão some)
   422   a lista de problemas que o servidor devolveu
   409   a mensagem do servidor (arquivo diferente, numerador, trava)
```

A tela guarda os arquivos do último envio **só em memória**: recarregou a página,
solte o LAST de novo.

## 4. Decisões de construção

```text
Angular 21        o 22 exige Node 22.22.3; as máquinas estão em 22.19
/api relativo     no desenvolvimento, proxy.conf.json repassa para a API; na
                  publicação, o servidor da tela faz o mesmo (a API não abre CORS)
fonte hospedada   @fontsource/barlow, sem Google Fonts (rede interna sem internet)
.npmrc            legacy-peer-deps (o npm 10.9 trava resolvendo o jsdom do Vitest)
sessão na aba     sessionStorage; senha nunca guardada; 401 volta para a entrada
datas sem Date    "2026-09-17" vira "17/09/2026" direto no texto; soma de dias em UTC
                  (a lição do fuso da cotação)
```

Visual: mesa de conferência. Concreto do cais, tinta, verde de contêiner para ação
e "pronto"; a faixa de segurança amarela e preta **só** onde há pendência. Tipo:
Barlow (a normal no texto, a condensada nos títulos).
