"""Confere cenários e previsões lendo os arquivos: soma, faixa em volta do ponto, resolução escrita e coerência entre as tabelas."""
from pathlib import Path

import pandas as pd

R = Path(__file__).resolve().parents[1] / "resultados"
c = pd.read_csv(R / "cenarios.csv").set_index("id")
p = pd.read_csv(R / "previsoes.csv").set_index("id")
assert c.chance_pct.sum() == 100
assert ((c.faixa_min <= c.chance_pct) & (c.chance_pct <= c.faixa_max)).all()
assert c.criterio_de_resolucao.notna().all() and p.como_resolver.notna().all()
assert p.chance_ia.between(0, 1).all()
# P12 acontece em C ou em parte de D: fica entre C e C + D
assert c.chance_pct["C"] <= p.chance_ia["P12"] * 100 <= c.chance_pct["C"] + c.chance_pct["D"]
assert abs(p.chance_ia["P13"] * 100 - c.chance_pct["D"]) < 0.01
# P06 com risco constante até 2029 (38 meses), tirando os mundos C, D e E, dá B
total = 1 - (1 - p.chance_ia["P06"]) ** (38 / 14)
b = total * (1 - (c.chance_pct["C"] + c.chance_pct["D"] + c.chance_pct["E"]) / 100)
assert abs(b * 100 - c.chance_pct["B"]) < 4, b
print("ok", round(b * 100, 1))
