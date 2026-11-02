"""Gera as tabelas leves da etapa E6 em dados/derivados/ a partir de dados/brutos/brasil/.

Nada aqui baixa nada: tudo sai dos arquivos registrados em dados/MANIFESTO_BRASIL.json.
A tabela curada de interrupções longas e a de orientação oficial são escritas à mão, com fonte, e não passam por aqui.

Uso: python ferramentas/derivar_brasil.py [fertilizantes diesel ipca energia conab conferir]   (sem nome, faz tudo)
"""
from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
BRUTOS = RAIZ / "dados" / "brutos" / "brasil"
DERIVADOS = RAIZ / "dados" / "derivados"

# Países cujo porto exportador de ureia fica dentro do Golfo Pérsico, ou seja, atrás do Estreito de Ormuz.
# É aproximação: o ComexStat dá o país de origem, não o porto de embarque. A Arábia Saudita tem porto no Mar Vermelho,
# os Emirados têm Fujairah e o Irã tem Chabahar, todos fora do estreito.
DENTRO_DO_GOLFO = {"Catar", "Arábia Saudita", "Irã", "Emirados Árabes Unidos", "Barein", "Coveite (Kuweit)", "Iraque"}
# Omã embarca ureia por Sur e Sohar, no Golfo de Omã, do lado de fora do estreito. Fica em grupo próprio.
FORA_DO_ESTREITO = {"Omã"}


def grupo_do_pais(pais: str) -> str:
    if pais in DENTRO_DO_GOLFO:
        return "dentro_do_golfo"
    if pais in FORA_DO_ESTREITO:
        return "oma_fora_do_estreito"
    return "resto_do_mundo"


def ler_comex(nome: str) -> list[dict]:
    return json.loads((BRUTOS / nome).read_text(encoding="utf-8"))["data"]["list"]


def fertilizantes() -> None:
    linhas = []
    for recorte, arq in (("ureia_ncm_31021010", "comex-ureia-pais.json"), ("capitulo_31_fertilizantes", "comex-cap31-pais.json")):
        for r in ler_comex(arq):
            linhas.append({"ano": int(r["year"]), "recorte": recorte, "pais": r["country"],
                           "valor_fob_usd": int(r["metricFOB"]), "kg": int(r["metricKG"])})
    d = pd.DataFrame(linhas)
    d["toneladas"] = d["kg"] / 1000
    d["grupo"] = d["pais"].map(grupo_do_pais)
    tot = d.groupby(["ano", "recorte"])[["valor_fob_usd", "toneladas"]].transform("sum")
    d["preco_medio_usd_t"] = (d["valor_fob_usd"] / d["toneladas"]).round(1)
    d["fatia_toneladas_pct"] = (100 * d["toneladas"] / tot["toneladas"]).round(2)
    total = d.groupby(["ano", "recorte"], as_index=False)[["valor_fob_usd", "toneladas"]].sum()
    total["pais"] = "TOTAL"
    total["grupo"] = "total"
    total["preco_medio_usd_t"] = (total["valor_fob_usd"] / total["toneladas"]).round(1)
    total["fatia_toneladas_pct"] = 100.0
    cols = ["ano", "recorte", "pais", "grupo", "valor_fob_usd", "toneladas", "preco_medio_usd_t", "fatia_toneladas_pct"]
    saida = pd.concat([d[cols], total[cols]]).sort_values(["recorte", "ano", "toneladas"], ascending=[True, True, False])
    saida["toneladas"] = saida["toneladas"].round(1)
    saida.to_csv(DERIVADOS / "brasil_fertilizantes.csv", index=False, encoding="utf-8")

    # resumo por ano: é a medida testável do "41% passou por Ormuz"
    res = []
    for (ano, recorte), g in d.groupby(["ano", "recorte"]):
        t = g["toneladas"].sum()
        por = g.groupby("pais")["toneladas"].sum()
        fatia = lambda *p: round(100 * sum(por.get(x, 0) for x in p) / t, 2)
        golfo = 100 * g.loc[g["grupo"] == "dentro_do_golfo", "toneladas"].sum() / t
        oma = 100 * g.loc[g["grupo"] == "oma_fora_do_estreito", "toneladas"].sum() / t
        res.append({"ano": ano, "recorte": recorte, "toneladas": round(t, 1), "valor_fob_usd": int(g["valor_fob_usd"].sum()),
                    "preco_medio_usd_t": round(g["valor_fob_usd"].sum() / t, 1),
                    "fatia_dentro_do_golfo_pct": round(golfo, 2), "fatia_oma_pct": round(oma, 2),
                    "fatia_golfo_mais_oma_pct": round(golfo + oma, 2), "fatia_ira_pct": fatia("Irã"),
                    "fatia_catar_pct": fatia("Catar"), "fatia_russia_pct": fatia("Rússia"), "fatia_nigeria_pct": fatia("Nigéria")})
    resumo = pd.DataFrame(res)
    # o outro código de ureia e a exportação, para medir quanto fica fora do recorte
    extra = []
    for chave, arq in (("ureia_outra_31021090_t", "comex-ureia-outra.json"), ("ureia_exportada_t", "comex-ureia-export.json")):
        for r in ler_comex(arq):
            extra.append({"ano": int(r["year"]), "chave": chave, "t": int(r["metricKG"]) / 1000})
    if extra:
        piv = pd.DataFrame(extra).pivot(index="ano", columns="chave", values="t").round(1).reset_index()
        resumo = resumo.merge(piv, on="ano", how="left")
        resumo.loc[resumo["recorte"] != "ureia_ncm_31021010", [c for c in piv.columns if c != "ano"]] = pd.NA
    resumo.sort_values(["recorte", "ano"]).to_csv(DERIVADOS / "brasil_fertilizantes_resumo.csv", index=False, encoding="utf-8")

    # mês a mês na crise de 2026
    arq = "comex-ureia-pais-mes-2025-2026.json"
    if (BRUTOS / arq).exists():
        m = pd.DataFrame(ler_comex(arq))
        m["t"] = m["metricKG"].astype(int) / 1000
        m["fob"] = m["metricFOB"].astype(int)
        m["mes"] = m["year"].astype(str) + "-" + m["monthNumber"].astype(str).str.zfill(2)
        m["grupo"] = m["country"].map(grupo_do_pais)
        p = m.pivot_table(index="mes", columns="grupo", values="t", aggfunc="sum", fill_value=0)
        p["toneladas"] = p.sum(axis=1)
        p["valor_fob_usd"] = m.groupby("mes")["fob"].sum()
        p["preco_medio_usd_t"] = (p["valor_fob_usd"] / p["toneladas"]).round(1)
        p["fatia_dentro_do_golfo_pct"] = (100 * p.get("dentro_do_golfo", 0) / p["toneladas"]).round(2)
        p["fatia_oma_pct"] = (100 * p.get("oma_fora_do_estreito", 0) / p["toneladas"]).round(2)
        p.round(1).reset_index().to_csv(DERIVADOS / "brasil_fertilizantes_mensal.csv", index=False, encoding="utf-8")
    print("fertilizantes ok")


def ipca() -> None:
    linhas = []
    for arq in ("sidra-1419-ipca-2018-2019.json", "sidra-7060-ipca-2020-2026.json"):
        tabela = re.search(r"sidra-(\d+)", arq).group(1)
        for r in json.loads((BRUTOS / arq).read_text(encoding="utf-8"))[1:]:
            if r["V"] in ("...", "-", "X"):
                continue
            linhas.append({"mes": r["D3C"][:4] + "-" + r["D3C"][4:], "tabela": tabela, "variavel": r["D2C"], "item": r["D4C"], "valor": float(r["V"])})
    d = pd.DataFrame(linhas)
    d["coluna"] = d["item"].map({"7171": "alim_dom", "7169": "geral"}) + d["variavel"].map({"63": "_mensal_pct", "2265": "_12m_pct"})
    p = d.pivot_table(index=["mes", "tabela"], columns="coluna", values="valor").reset_index()
    p = p[p["mes"] >= "2019-01"].sort_values("mes")
    # conta própria dos 12 meses: encadeia a variação mensal e confere contra o número publicado
    base = d[(d["item"] == "7171") & (d["variavel"] == "63")].set_index("mes")["valor"].sort_index()
    conta = ((1 + base / 100).rolling(12).apply(lambda x: x.prod(), raw=True) - 1) * 100
    p["alim_dom_12m_recalculado_pct"] = p["mes"].map(conta).round(2)
    p = p[["mes", "tabela", "alim_dom_mensal_pct", "alim_dom_12m_pct", "alim_dom_12m_recalculado_pct", "geral_mensal_pct", "geral_12m_pct"]]
    if (DERIVADOS / "brasil_diesel_mensal.csv").exists():
        dz = pd.read_csv(DERIVADOS / "brasil_diesel_mensal.csv")
        p = p.merge(dz, on="mes", how="left")
    p.to_csv(DERIVADOS / "brasil_ipca_alimentos.csv", index=False, encoding="utf-8")
    print("ipca ok", p["mes"].min(), p["mes"].max())


def diesel() -> None:
    bruto = pd.read_excel(BRUTOS / "anp-precos-mensal-brasil-desde-2013.xlsx", header=None)
    ini = bruto.index[bruto[1].astype(str).str.upper().eq("PRODUTO")][0]
    d = bruto.iloc[ini + 1 :].copy()
    d.columns = [str(c).strip() for c in bruto.iloc[ini]]
    mes_col, prod, preco = d.columns[0], "PRODUTO", [c for c in d.columns if "MÉDIO REVENDA" in c.upper() or "MEDIO REVENDA" in c.upper()][0]
    d["mes"] = pd.to_datetime(d[mes_col]).dt.strftime("%Y-%m")
    d = d[d[prod].astype(str).str.upper().isin(["OLEO DIESEL", "OLEO DIESEL S10"]) & (d["mes"] >= "2019-01")]
    d[preco] = pd.to_numeric(d[preco], errors="coerce")
    p = d.pivot_table(index="mes", columns=prod, values=preco).reset_index()
    p.columns = [{"OLEO DIESEL": "diesel_comum_rs_l", "OLEO DIESEL S10": "diesel_s10_rs_l"}.get(c, c) for c in p.columns]
    p.columns.name = None
    p.to_csv(DERIVADOS / "brasil_diesel_mensal.csv", index=False, encoding="utf-8")
    print("diesel ok", p["mes"].min(), p["mes"].max())


# Conferido nos dados: DEC = DECIND + DECIP. O número que a ANEEL divulga deixa de fora o dia crítico, a situação de
# emergência, o racionamento e o fator externo. As outras parcelas somadas dão o tempo que a pessoa ficou sem luz.
PARCELAS_FORA_DO_DEC = {
    "dec_situacao_emergencia_horas": ["DECINE"],
    "dec_dia_critico_horas": ["DECINC", "DECIPC", "DECXNC", "DECXPC"],
    "dec_externo_e_ons_horas": ["DECINO", "DECXN", "DECXP"],
}
CODIGOS = ["DEC", "FEC", "NumCon", "DECIND", "DECIP"] + [c for v in PARCELAS_FORA_DO_DEC.values() for c in v]


def energia() -> None:
    partes = []
    for arq in ("aneel-continuidade-2010-2019.zip", "aneel-continuidade-2020-2029.zip"):
        with zipfile.ZipFile(BRUTOS / arq) as z, z.open(z.namelist()[0]) as f:
            for bloco in pd.read_csv(f, sep=";", encoding="utf-8", dtype=str, chunksize=2_000_000,
                                     usecols=["IdeConjUndConsumidoras", "DscConjUndConsumidoras", "SigAgente", "SigIndicador", "AnoIndice", "NumPeriodoIndice", "VlrIndiceEnviado"]):
                b = bloco[bloco["SigIndicador"].isin(CODIGOS) & (bloco["AnoIndice"] >= "2015") & (bloco["AnoIndice"] <= "2026")].copy()
                if not b.empty:
                    b["v"] = pd.to_numeric(b["VlrIndiceEnviado"].str.replace(",", ".", regex=False), errors="coerce")
                    partes.append(b.drop(columns="VlrIndiceEnviado"))
    d = pd.concat(partes)
    d["SigAgente"] = d["SigAgente"].str.strip()
    d["ano"] = d["AnoIndice"].astype(int)
    d["mes"] = d["NumPeriodoIndice"].astype(int)
    d = d[d["mes"].between(1, 12)]
    chave = ["SigAgente", "IdeConjUndConsumidoras", "DscConjUndConsumidoras", "ano", "mes"]
    p = d.pivot_table(index=chave, columns="SigIndicador", values="v", aggfunc="max").reset_index()
    p = p[p["NumCon"].fillna(0) > 0]
    for c in CODIGOS:
        if c not in p:
            p[c] = 0.0
    p[CODIGOS] = p[CODIGOS].fillna(0.0)
    for nome, codigos in PARCELAS_FORA_DO_DEC.items():
        p[nome] = p[codigos].sum(axis=1)
    p["dec_total_com_expurgos_horas"] = p["DEC"] + p[list(PARCELAS_FORA_DO_DEC)].sum(axis=1)
    medidas = {"dec_horas": "DEC", "fec_vezes": "FEC", "dec_programada_horas": "DECIP"}
    medidas.update({n: n for n in PARCELAS_FORA_DO_DEC})
    medidas["dec_total_com_expurgos_horas"] = "dec_total_com_expurgos_horas"

    def consolidar(g: pd.DataFrame) -> pd.Series:
        # média do mês ponderada pelos consumidores do conjunto, somada nos meses do ano
        cons = g.groupby("mes")["NumCon"].sum()
        s = {nome: ((g[col] * g["NumCon"]).groupby(g["mes"]).sum() / cons).sum() for nome, col in medidas.items()}
        s["consumidores_media"] = cons.mean()
        s["meses"] = g["mes"].nunique()
        s["conjuntos"] = g["IdeConjUndConsumidoras"].nunique()
        return pd.Series(s)

    brasil = p.groupby("ano").apply(consolidar, include_groups=False).reset_index()
    brasil.insert(1, "agente", "BRASIL")
    por_agente = p.groupby(["ano", "SigAgente"]).apply(consolidar, include_groups=False).reset_index().rename(columns={"SigAgente": "agente"})
    saida = pd.concat([brasil, por_agente]).sort_values(["ano", "agente"])
    saida[list(medidas)] = saida[list(medidas)].round(2)
    for c in ("consumidores_media", "meses", "conjuntos"):
        saida[c] = saida[c].round(0).astype("int64")
    saida.to_csv(DERIVADOS / "brasil_energia_dec.csv", index=False, encoding="utf-8")

    # a pior experiência de cada ano: o conjunto de unidades consumidoras com mais horas sem luz em um único mês
    grandes = p[p["NumCon"] >= 5000]
    piores = grandes.sort_values("dec_total_com_expurgos_horas", ascending=False).groupby("ano").head(5)
    piores = piores[["ano", "mes", "SigAgente", "DscConjUndConsumidoras", "dec_total_com_expurgos_horas", "DEC", "NumCon"]].rename(
        columns={"SigAgente": "agente", "DscConjUndConsumidoras": "conjunto", "dec_total_com_expurgos_horas": "horas_no_mes_total",
                 "DEC": "horas_no_mes_dec_divulgado", "NumCon": "consumidores"})
    # um mês tem no máximo 744 horas: acima disso é erro de envio da distribuidora, e não entra como fato
    piores["acima_de_um_mes_inteiro"] = piores["horas_no_mes_total"] > 744
    piores.sort_values(["ano", "horas_no_mes_total"], ascending=[True, False]).round(2).to_csv(DERIVADOS / "brasil_energia_piores_meses.csv", index=False, encoding="utf-8")

    # o que o indicador registrou no mês de cada grande caso da tabela curada
    casos = [("CEA", 2020, 11, "apagão do Amapá"), ("ELETROPAULO", 2023, 11, "Enel SP nov/2023"), ("ELETROPAULO", 2024, 10, "Enel SP out/2024"),
             ("ELETROPAULO", 2025, 12, "Enel SP dez/2025"), ("CEEE-D", 2024, 5, "enchentes do RS"), ("RGE SUL", 2024, 5, "enchentes do RS")]
    linhas_casos = []
    for agente, ano, mes, caso in casos:
        g = p[(p["SigAgente"] == agente) & (p["ano"] == ano) & (p["mes"] == mes)]
        if g.empty:
            continue
        cons = g["NumCon"].sum()
        media = lambda col: round(float((g[col] * g["NumCon"]).sum() / cons), 2)
        linhas_casos.append({"caso": caso, "agente": agente, "ano": ano, "mes": mes, "consumidores": int(cons),
                             "dec_divulgado_horas_no_mes": media("DEC"), "dec_total_com_expurgos_horas_no_mes": media("dec_total_com_expurgos_horas"),
                             "dec_situacao_emergencia_horas_no_mes": media("dec_situacao_emergencia_horas"), "dec_dia_critico_horas_no_mes": media("dec_dia_critico_horas"),
                             "dec_externo_e_ons_horas_no_mes": media("dec_externo_e_ons_horas")})
    pd.DataFrame(linhas_casos).to_csv(DERIVADOS / "brasil_energia_meses_dos_casos.csv", index=False, encoding="utf-8")
    print(pd.DataFrame(linhas_casos).to_string())
    print("energia ok")
    print(brasil.round(2).to_string())
    print(piores.head(40).to_string())
    print("confere DEC = DECIND + DECIP:", ((p["DEC"] - p["DECIND"] - p["DECIP"]).abs() > 0.02).mean())


MESES = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]


def conab() -> None:
    from pypdf import PdfReader

    linhas = []
    for pagina in PdfReader(BRUTOS / "conab-serie-historica-estoques-set2026.pdf").pages:
        texto = pagina.extract_text()
        for m in re.finditer(r"Tabela\s+\d+\s*[-–]\s*Estoque Total de ([^\n]*?)\s*(?:-\s*Brasil\s*)?[-–]\s*em\s*tonelada(.*?)(?=Tabela\s+\d+\s*[-–]|\Z)", texto, re.S):
            produto = m.group(1).strip()
            for linha in m.group(2).splitlines():
                c = linha.split()
                if len(c) >= 2 and re.fullmatch(r"(19|20)\d\d", c[0]) and all(re.fullmatch(r"[\d.]+", x) for x in c[1:13]):
                    valores = [int(x.replace(".", "")) for x in c[1:13]]
                    linhas.append((produto, int(c[0]), valores))
    registros = []
    for produto, ano, valores in linhas:
        if ano < 2015:
            continue
        r = {"ano": ano, "produto": produto, "fonte": "Conab, Série histórica de estoques públicos, setembro de 2026",
             "ultimo_mes": MESES[len(valores) - 1], "estoque_ultimo_mes_t": valores[-1], "media_do_ano_t": round(sum(valores) / len(valores))}
        r.update({f"t_{mes.lower()}": v for mes, v in zip(MESES, valores)})
        registros.append(r)
    pd.DataFrame(registros).sort_values(["produto", "ano"]).to_csv(DERIVADOS / "brasil_estoques_conab.csv", index=False, encoding="utf-8")
    print("conab ok", sorted({r["produto"] for r in registros}), len(registros))


def conferir() -> None:
    """Confere totais contra uma segunda fonte e grava o resultado em dados/derivados/brasil_conferencia.md."""
    txt = ["# Conferência da etapa E6", "",
           "Gerado por `ferramentas/derivar_brasil.py conferir`. Compara o que saiu das tabelas com uma segunda fonte.", ""]
    # 1. ureia: ComexStat contra UN Comtrade (HS 310210 reúne os códigos 31021010 e 31021090)
    res = pd.read_csv(DERIVADOS / "brasil_fertilizantes_resumo.csv")
    res = res[res["recorte"] == "ureia_ncm_31021010"].set_index("ano")
    txt += ["## 1. Ureia importada: ComexStat contra UN Comtrade", "", "| ano | ComexStat, 31021010 + 31021090 (t) | Comtrade, HS 310210 (t) | diferença |", "|---|---|---|---|"]
    for ano in (2022, 2023, 2024, 2025):
        arq = BRUTOS / f"comtrade-310210-brasil-{ano}.json"
        dados = json.loads(arq.read_text(encoding="utf-8")).get("data", []) if arq.exists() else []
        mundo = [r for r in dados if r.get("partnerCode") == 0]
        t = sum(float(r.get("netWgt") or 0) for r in mundo) / 1000 or None
        cs = res.loc[ano, "toneladas"] + res.loc[ano, "ureia_outra_31021090_t"]
        txt.append(f"| {ano} | {cs:,.0f} | {t:,.0f} | {100 * (t / cs - 1):+.2f}% |" if t else f"| {ano} | {cs:,.0f} | sem dado | |")
    ano25 = res.loc[2025]
    txt += ["", "## 2. Ureia em 2025: ComexStat contra a InfoMoney/Reuters (dados oficiais citados em 02/03/2026)", "",
            "| medida | este projeto | InfoMoney |", "|---|---|---|",
            f"| total importado | {ano25['toneladas'] / 1e6:.2f} mi t | cerca de 7,7 mi t |",
            f"| Oriente Médio, com Omã | {ano25['fatia_golfo_mais_oma_pct'] * ano25['toneladas'] / 1e8:.2f} mi t | cerca de 2,7 mi t |",
            f"| Irã | {ano25['fatia_ira_pct']:.2f}% | cerca de 2% |", ""]
    # 3. IPCA: SIDRA contra Banco Central, e 12 meses publicados contra o encadeado
    ip = pd.read_csv(DERIVADOS / "brasil_ipca_alimentos.csv")
    bc = pd.DataFrame(json.loads((BRUTOS / "bcb-sgs-27864-alimentacao-domicilio.json").read_text(encoding="utf-8")))
    bc["mes"] = bc["data"].str[6:] + "-" + bc["data"].str[3:5]
    bc["bcb"] = bc["valor"].astype(float)
    j = ip.merge(bc[["mes", "bcb"]], on="mes")
    dif = (j["alim_dom_mensal_pct"] - j["bcb"]).abs()
    dif12 = (ip["alim_dom_12m_pct"] - ip["alim_dom_12m_recalculado_pct"]).abs().dropna()
    txt += ["## 3. IPCA alimentação no domicílio: IBGE SIDRA contra Banco Central SGS 27864", "",
            f"{len(j)} meses comparados, de {j['mes'].min()} a {j['mes'].max()}. Maior diferença na variação mensal: {dif.max():.2f} ponto; meses diferentes: {(dif > 0.001).sum()}.",
            f"Os 12 meses publicados contra o encadeamento das variações mensais: maior diferença {dif12.max():.2f} ponto em {len(dif12)} meses.", ""]
    # 4. DEC: a conta ponderada contra o número divulgado pela ANEEL
    en = pd.read_csv(DERIVADOS / "brasil_energia_dec.csv")
    br = en[en["agente"] == "BRASIL"].set_index("ano")
    txt += ["## 4. DEC e FEC Brasil: conta ponderada contra o divulgado pela ANEEL (eixos)", "", "| medida | este projeto | ANEEL | diferença |", "|---|---|---|---|"]
    for ano, col, nome, an in ((2024, "dec_horas", "DEC 2024 (horas)", 10.24), (2023, "dec_horas", "DEC 2023 (horas)", 10.42), (2024, "fec_vezes", "FEC 2024", 4.89), (2023, "fec_vezes", "FEC 2023", 5.15)):
        v = br.loc[ano, col]
        txt.append(f"| {nome} | {v:.2f} | {an:.2f} | {100 * (v / an - 1):+.2f}% |")
    txt += ["", "O projeto pondera por conjunto com o NumCon de cada mês; a regra exata da ANEEL não está no dicionário do dado.", ""]
    # 5. Conab: a tabela oficial contra a Compre Rural (08/09/2026), que citou o levantamento de julho
    co = pd.read_csv(DERIVADOS / "brasil_estoques_conab.csv")
    co = co[co["ano"] == 2026].set_index("produto")
    txt += ["## 5. Estoques públicos de julho de 2026: Conab contra a Compre Rural", "", "| produto | Conab (t) | Compre Rural |", "|---|---|---|"]
    for prod, cr in (("Arroz", "293 toneladas"), ("Feijão", "207 toneladas"), ("Trigo", "6,6 mil toneladas"), ("Milho", "125,5 mil toneladas")):
        txt.append(f"| {prod} | {int(co.loc[prod, 't_jul']):,} | {cr} |")
    txt += ["", "O arroz não bate: o PDF da Conab traz 293.800 toneladas em julho, mil vezes o que a matéria diz. Os outros três produtos batem, então o provável é a matéria ter lido 293.800 como 293,8; é inferência minha. Quem usar a matéria dirá que o estoque de arroz está zerado, e não está.", ""]
    (DERIVADOS / "brasil_conferencia.md").write_text("\n".join(txt), encoding="utf-8")
    print("\n".join(txt))


GRUPOS = {"fertilizantes": fertilizantes, "diesel": diesel, "ipca": ipca, "energia": energia, "conab": conab, "conferir": conferir}


def main() -> None:
    DERIVADOS.mkdir(parents=True, exist_ok=True)
    for g in sys.argv[1:] or GRUPOS:
        GRUPOS[g]()


if __name__ == "__main__":
    main()
