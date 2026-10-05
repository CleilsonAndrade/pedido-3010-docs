#!/usr/bin/env python3
from pathlib import Path

ACTIVE_DOCS = [
    '00_STATUS/STATUS_PEDIDO_3010.md',
    '01_ARQUITETURA/VISAO_GERAL.md',
    '01_ARQUITETURA/FRONTEIRA_COMEX_API_WINTHOR.md',
    '01_ARQUITETURA/AUTENTICACAO_WINTHOR.md',
    '02_FLUXOS/PREVIA_DOS_LASTS.md',
    '02_FLUXOS/CALCULO_DO_PEDIDO.md',
    '02_FLUXOS/GRAVACAO_NA_3010.md',
    '02_FLUXOS/TELA_DE_CONFERENCIA.md',
    '03_ESPECIFICACOES/ESP_PEDIDO_MASTER.md',
    '04_VALIDACOES/EVIDENCIAS_TRACE_E_BANCO.md',
    '04_VALIDACOES/ROTEIRO_QTSUGESTAO.md',
    '04_VALIDACOES/VALIDACAO_HOMOLOGACAO_RODADAS.md',
    '04_VALIDACOES/VALIDACAO_TEMPLATE_X_TRACE.md',
    '04_VALIDACOES/VALIDACAO_PRIMEIRO_PEDIDO_GRAVADO.md',
    '04_VALIDACOES/VALIDACAO_TIME_IMPORTACAO_3_LASTS.md',
    '05_CONTRATOS/CONTRATO_COMEX_API.md',
    '05_CONTRATOS/CONTRATO_API_PEDIDO_3010.md',
    '05_CONTRATOS/COLUNAS_PCPEDIDO_PCITEM.md',
    '06_OPERACAO/CONFIGURACAO_E_EXECUCAO.md',
    '06_OPERACAO/ROTEIRO_HOMOLOGACAO.md',
    '06_OPERACAO/BASE_TESTE.md',
    '06_OPERACAO/SERVIDOR_E_PUBLICACAO.md',
    '07_DECISOES/DECISOES.md',
    'CHANGELOG.md',
    'README.md',
]

EXCLUDED_TOP_LEVEL_DIRS = {
    '99_HISTORICO',
}

root = Path(__file__).resolve().parents[1]
out = root / "DOCUMENTACAO_ATIVA_COMPLETA.txt"
missing = [doc for doc in ACTIVE_DOCS if not (root / doc).is_file()]
if missing:
    raise SystemExit("Documentos ausentes:\n- " + "\n- ".join(missing))
fora = []

for p in root.rglob("*.md"):
    rel = p.relative_to(root)

    if ".git" in p.parts:
        continue

    if rel.parts and rel.parts[0] in EXCLUDED_TOP_LEVEL_DIRS:
        continue

    rel_str = str(rel)

    if rel_str not in ACTIVE_DOCS:
        fora.append(rel_str)

fora.sort()
if fora:
    raise SystemExit("Documentos fora da lista ACTIVE_DOCS:\n- " + "\n- ".join(fora))
sep = "=" * 100
parts = []
for index, doc in enumerate(ACTIVE_DOCS, 1):
    body = (root / doc).read_bytes()
    header = (f"{sep}\nDOCUMENTO {index:02d}/{len(ACTIVE_DOCS):02d}: {doc}\n{sep}\n\n").encode("utf-8")
    part = header + body
    if not part.endswith(b"\n"):
        part += b"\n"
    parts.append(part)
out.write_bytes(b"\n".join(parts))
print(f"Consolidado regenerado: {len(ACTIVE_DOCS)}/{len(ACTIVE_DOCS)} documentos.")
