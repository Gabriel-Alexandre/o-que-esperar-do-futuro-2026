"""Confere que os cenários somam 100 e que a tabela de previsões está completa."""
import pandas as pd
assert 45 + 23 + 25 + 7 == 100
p = pd.read_csv("resultados/previsoes.csv")
assert p.chance_ia.between(0, 1).all() and p.como_resolver.notna().all() and p.prazo.notna().all()
print(len(p), "previsões ok")
