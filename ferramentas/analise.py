"""Toda a conta do relatório: taxa-base, sinais, termômetro de guerra, hipóteses e o que circula. Grava resultados/RESUMO.json."""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

RAIZ = Path(__file__).resolve().parents[1]
DER = RAIZ / "dados" / "derivados"
SAIDA = RAIZ / "resultados"

# capital (lat, lon); fonte: coordenadas públicas de capitais
CAPITAIS = {"GBR": (51.5, -0.1), "IRL": (53.3, -6.3), "FRA": (48.9, 2.4), "DEU": (52.5, 13.4), "NLD": (52.4, 4.9), "DNK": (55.7, 12.6),
            "NOR": (59.9, 10.8), "SWE": (59.3, 18.1), "FIN": (60.2, 24.9), "EST": (59.4, 24.8), "LVA": (57.0, 24.1), "LTU": (54.7, 25.3),
            "POL": (52.2, 21.0), "CZE": (50.1, 14.4), "AUT": (48.2, 16.4), "CHE": (46.9, 7.4), "HRV": (45.8, 16.0), "USA": (38.9, -77.0),
            "CAN": (45.4, -75.7), "MEX": (19.4, -99.1), "CHL": (-33.4, -70.7), "COL": (4.7, -74.1), "ARG": (-34.6, -58.4), "BRA": (-15.8, -47.9),
            "ZAF": (-25.7, 28.2), "JPN": (35.7, 139.7), "TWN": (25.0, 121.5), "ISR": (31.8, 35.2), "IND": (28.6, 77.2), "PHL": (14.6, 121.0),
            "SGP": (1.3, 103.8), "NZL": (-41.3, 174.8), "AUS": (-35.3, 149.1), "BEL": (50.8, 4.4), "PRT": (38.7, -9.1), "ESP": (40.4, -3.7), "ITA": (41.9, 12.5)}
# território russo de referência: Moscou, São Petersburgo, Kaliningrado e Vladivostok
RUSSIA = [(55.8, 37.6), (59.9, 30.3), (54.7, 20.5), (43.1, 131.9)]


def km(a, b) -> float:
    la1, lo1, la2, lo2 = map(math.radians, (*a, *b))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (round((c - m) / d, 3), round((c + m) / d, 3))


def taxa(df: pd.DataFrame, coluna: str) -> dict:
    fechado = df[df[coluna].isin(["sim", "nao"])]
    k, n = int((fechado[coluna] == "sim").sum()), len(fechado)
    return {"k": k, "n": n, "pct": round(100 * k / n, 1) if n else None, "ic95": wilson(k, n)}


def historia() -> dict:
    e0 = pd.read_csv(DER / "historia_episodios.csv", dtype=str)
    e0["pais_unico"] = e0.pais.replace({"Alemanha Ocidental": "Alemanha"})
    e = e0[e0.entra_na_taxa == "sim"]
    primeiro = e.sort_values("ano_mes").drop_duplicates("pais_unico")
    sem = e[e.sinais_na_data_do_pedido == "nao"]
    com = e[e.sinais_na_data_do_pedido == "sim"]
    casos = e0[e0.id.isin(["UA-2021", "IN-2025", "CN-1969"])]
    com_casos = pd.concat([sem, casos])
    iniciadores_e_malvinas = {"JP-1937", "DE-1935", "UK-1980"}
    recortes = {"todos": e, "com_sinais_duros": com, "sem_sinais_duros": sem, "ameaca_estatal": e[e.ameaca_estatal == "sim"], "primeiro_de_cada_pais": primeiro,
                "depois_de_2000": e[e.ano_mes.str[:4].astype(int) >= 2000]}
    r = {nome: {"24m": taxa(d, "guerra_no_territorio_24m"), "60m": taxa(d, "guerra_no_territorio_60m"), "episodios": len(d)} for nome, d in recortes.items()}
    r["atacado_por_quem_temia_60m"] = taxa(e[e.guerra_no_territorio_60m.isin(["sim", "nao"])], "guerra_com_o_ameacante_declarado")
    # o número que mais depende de escolha: só o pedido, guerra no território em 60 meses
    r["faixa_so_o_pedido_60m"] = {
        "sem iniciadores nem Malvinas": taxa(sem[~sem.id.isin(iniciadores_e_malvinas)], "guerra_no_territorio_60m"),
        "regra principal": taxa(sem, "guerra_no_territorio_60m"),
        "um voto por país": taxa(sem.sort_values("ano_mes").drop_duplicates("pais_unico"), "guerra_no_territorio_60m"),
        "contando os 3 estudos de caso": taxa(com_casos, "guerra_no_territorio_60m"),
        "estudos de caso e um voto por país": taxa(com_casos.sort_values("ano_mes").drop_duplicates("pais_unico"), "guerra_no_territorio_60m"),
    }
    r["episodios_na_taxa"] = len(e)
    r["estudos_de_caso"] = casos.id.tolist()
    r["guerras_sem_campanha"] = len(pd.read_csv(DER / "guerras_sem_campanha.csv"))
    return r


def sinais() -> list[dict]:
    s = pd.read_csv(DER / "sinais.csv")
    pontos = {"sim": 1.0, "parcial": 0.5, "nao": 0.0}
    saida = []
    for (mom, pais), g in s.groupby(["momento", "pais"]):
        v = g[g.valor.isin(pontos)]
        saida.append({"momento": mom, "pais": pais, "pontos": float(v.valor.map(pontos).sum()), "de": len(v), "sem_dado": int((g.valor == "sem_dado").sum()),
                      "sim": int((g.valor == "sim").sum())})
    return saida


def paises() -> dict:
    p = pd.read_csv(DER / "paises.csv")
    lista = p[p.na_lista_newsweek == "sim"]
    nac = p[(p.abrangencia == "nacional") & p.prazo_max_dias.notna() & p.iso3.isin(CAPITAIS)].copy()
    nac["km_russia"] = nac.iso3.map(lambda i: min(km(CAPITAIS[i], r) for r in RUSSIA))
    rho_todos = spearmanr(nac.km_russia, nac.prazo_max_dias)
    eur = nac[nac.continente == "Europa"]
    rho_eur = spearmanr(eur.km_russia, eur.prazo_max_dias)
    com_guerra = p[p.iso3.isin(CAPITAIS) & p.menciona_guerra.isin(["sim", "nao"])].copy()
    com_guerra["km_russia"] = com_guerra.iso3.map(lambda i: min(km(CAPITAIS[i], r) for r in RUSSIA))
    nac[["pais", "iso3", "continente", "prazo_min_dias", "prazo_max_dias", "km_russia", "menciona_guerra"]].round(0).to_csv(SAIDA / "termometro.csv", index=False)
    ano = lista.data_primeira_orientacao.dropna().astype(str).str[:4].astype(int)
    faixas = lista.prazo_max_dias
    return {"na_lista": len(lista), "por_abrangencia": lista.abrangencia.value_counts().to_dict(), "com_data_primeira": int(ano.size), "antes_de_2022": int((ano < 2022).sum()),
            "de_2022_em_diante": int((ano >= 2022).sum()), "em_2026": int((ano >= 2026).sum()), "menciona_guerra": int((lista.menciona_guerra == "sim").sum()),
            "com_prazo": int(faixas.notna().sum()), "ate_3_dias": int((faixas <= 3).sum()), "de_7_a_14": int((faixas >= 7).sum()), "mediana_dias": float(faixas.median()),
            "termometro": {"n": len(nac), "spearman_todos": round(float(rho_todos.statistic), 2), "p_todos": round(float(rho_todos.pvalue), 3),
                           "n_europa": len(eur), "spearman_europa": round(float(rho_eur.statistic), 2), "p_europa": round(float(rho_eur.pvalue), 3)},
            "km_mediana_cita_guerra": round(float(com_guerra[com_guerra.menciona_guerra == "sim"].km_russia.median())), "km_mediana_nao_cita": round(float(com_guerra[com_guerra.menciona_guerra == "nao"].km_russia.median()))}


def hipoteses() -> dict:
    h = pd.read_csv(DER / "hipoteses_evidencias.csv")
    b = pd.read_csv(DER / "hipoteses_segundo_codificador.csv").set_index("id").loc[h.id]
    pesos = {"alto": 2, "medio": 1, "baixo": 0.5}
    cols = [c for c in h.columns if c.startswith("H")]
    saida = []
    for c in cols:
        saida.append({"hipotese": c, "contra_1": float(h[h[c] == "I"].peso.map(pesos).sum()), "a_favor_1": float(h[h[c] == "C"].peso.map(pesos).sum()),
                      "contra_2": float(h.peso.map(pesos)[b[c].values == "I"].sum()), "a_favor_2": float(h.peso.map(pesos)[b[c].values == "C"].sum())})
    saida.sort(key=lambda x: -(x["contra_1"] + x["contra_2"]))
    pd.DataFrame(saida).to_csv(SAIDA / "hipoteses.csv", index=False)
    iguais = sum(int((h[c].values == b[c].values).sum()) for c in cols)
    return {"tabela": saida, "celulas": len(h) * len(cols), "celulas_iguais": iguais, "pct_iguais": round(100 * iguais / (len(h) * len(cols)), 1)}


def brasil() -> dict:
    r = pd.read_csv(DER / "brasil_fertilizantes_resumo.csv")
    u = r[r.recorte.str.contains("ureia")].set_index("ano")
    ip = pd.read_csv(DER / "brasil_ipca_alimentos.csv")
    m = pd.read_csv(DER / "brasil_fertilizantes_mensal.csv")
    d = pd.read_csv(DER / "brasil_interrupcoes_longas.csv")
    return {"ureia_2025_t": float(u.loc[2025].toneladas), "golfo_2025_pct": float(u.loc[2025].fatia_dentro_do_golfo_pct), "oma_2025_pct": float(u.loc[2025].fatia_oma_pct), "golfo_2026_pct": float(u.loc[2026].fatia_dentro_do_golfo_pct),
            "oma_2026_pct": float(u.loc[2026].fatia_oma_pct), "preco_pico_usd": float(m.preco_medio_usd_t.max()), "preco_pico_mes": m.mes[m.preco_medio_usd_t.idxmax()], "preco_ultimo_usd": float(m.preco_medio_usd_t.iloc[-1]), "preco_ultimo_mes": m.mes.iloc[-1],
            "alimentos_12m_ultimo_pct": float(ip.alim_dom_12m_pct.iloc[-1]), "alimentos_ultimo_mes": ip.mes.iloc[-1], "alimentos_fev_2026_pct": float(ip[ip.mes == "2026-02"].alim_dom_12m_pct.iloc[0]),
            "casos_com_dias": int(d.dias_sem_servico.notna().sum()), "casos": len(d), "casos_com_ataque": int((d.foi_ataque.astype(str).str.lower() == "sim").sum()), "maior_dias": float(d.dias_sem_servico.max())}


def videos() -> dict:
    a = pd.read_csv(DER / "videos_afirmacoes.csv")
    r = pd.read_csv(DER / "videos_resumo.csv")
    return {"videos": int(a.video.nunique()), "afirmacoes": len(a), "por_selo": a.selo.value_counts().to_dict(), "views_somadas": int(pd.to_numeric(r.views, errors="coerce").sum()),
            "vendem_algo": int(r.vende_algo.astype(str).str.lower().str.startswith("sim").sum()), "dizem_guerra_vem": int(r.diz_que_guerra_vem.astype(str).str.lower().str.startswith("sim").sum())}


def mercados() -> list[dict]:
    m = pd.read_csv(DER / "mercados.csv")
    alvos = ["Will Russia invade a NATO country by December 31, 2026?", "Russia military action against an EU country by December 31, 2026?", "Russia military action against an EU country by December 31, 2027?",
             "NATO x Russia military clash by December 31, 2026?", "NATO article 5 before 2027?", "Will China invade Taiwan by December 31, 2027?", "Will Strait of Hormuz traffic not return to normal in 2026?", "US x Russia military clash by December 31, 2026?"]
    return m[m.pergunta.isin(alvos)].drop_duplicates("pergunta")[["pergunta", "chance_sim", "fim", "volume_usd", "data_foto"]].to_dict("records")


def main() -> None:
    SAIDA.mkdir(exist_ok=True)
    resumo = {"historia": historia(), "sinais": sinais(), "paises": paises(), "hipoteses": hipoteses(), "videos": videos(), "mercados": mercados(), "brasil": brasil()}
    (SAIDA / "RESUMO.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(resumo, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
