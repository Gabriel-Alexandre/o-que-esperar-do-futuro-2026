"""Procura travessão e frases que o projeto não diz nos textos que o público lê."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
ARQ = ["README.md", "RELATORIO.md", "RESUMO_SIMPLES.md", "ESTADO.md", "docs/PLANO.md", "docs/PREVISOES.md", "docs/LEITURA_DA_IA.md", "docs/RODADAS.md", "resultados/cenarios.csv"]
PROIBIDO = ["—", "a guerra vai", "vai haver guerra", "compre ", "invista "]
ruim = 0
for a in ARQ:
    t = (RAIZ / a).read_text(encoding="utf-8").lower()
    for p in PROIBIDO:
        if p in t:
            print(a, repr(p))
            ruim += 1
print("problemas:", ruim)
raise SystemExit(1 if ruim else 0)
