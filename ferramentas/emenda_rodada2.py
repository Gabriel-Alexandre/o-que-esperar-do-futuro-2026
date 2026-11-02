"""Rodada 2: aplica à base os consertos da revisão adversarial de 02/nov/2026 (docs/REVISAO_ADVERSARIAL.md). Roda uma vez; cada troca está em docs/RODADAS.md."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

D = Path(__file__).resolve().parents[1] / "dados" / "derivados"


def episodios() -> None:
    e = pd.read_csv(D / "historia_episodios.csv", dtype=str)
    # falham a própria regra: emissor local, exercício no dia do ataque, conflito já aberto
    fora = {"UA-2021": "emissor é vice-prefeito de Kyiv e o sinal veio dias antes da invasão; fica como estudo de caso",
            "IN-2025": "exercício de sirene no dia dos ataques; fica como estudo de caso",
            "CN-1969": "pedido coletivo depois de o conflito começar; fica como estudo de caso"}
    e["entra_na_taxa"] = e.id.map(lambda i: "nao" if i in fora or i == "EU-2025" else "sim")
    e["motivo_fora"] = e.id.map(lambda i: fora.get(i, "supranacional" if i == "EU-2025" else ""))
    e["sinais_na_data_do_pedido"] = e.apply(lambda l: "nao" if l.id in fora else l.houve_sinais_duros, axis=1)
    ameacante = {"UK-1938", "UK-1939", "IL-1990"}
    e["guerra_com_o_ameacante_declarado"] = e.apply(lambda l: "sim" if l.id in ameacante else ("aberto" if l.guerra_no_territorio_60m == "aberto" else "nao"), axis=1)
    e.loc[e.id == "DK-2024", "ano_mes"] = "2024-06"
    e.loc[e.id == "DK-2024", "observacao"] = "Nota oficial de 15/06/2024 em oficiais/dnk-brs2024."
    e.loc[e.id == "PL-2025", "observacao"] = "Drones russos em set/2025 ficam fora: abatidos sem alvo declarado em território polonês, régua da emenda da rodada 2. A régua de drone com alvo conta (P04, P12)."
    novos = [("IE-2019", "Irlanda", "2019-10"), ("EE-2018", "Estônia", "2018-11"), ("LV-2020", "Letônia", "2020-06"), ("CA-2007", "Canadá", "2007-01"),
             ("MX-2018", "México", "2018-01"), ("AR-2018", "Argentina", "2018-11"), ("IT-2012", "Itália", "2012-06"), ("BE-2018", "Bélgica", "2018-12"), ("PL-2022", "Polônia", "2022-01")]
    p = pd.read_csv(D / "paises.csv", dtype=str).set_index("pais")
    linhas = []
    for i, pais, data in novos:
        origem = p.loc[pais]
        ano = int(data[:4])
        linhas.append({"id": i, "pais": pais, "ano_mes": data, "nome": str(origem.titulo_documento), "tipo_pedido": "estoque ou kit em casa", "motivo_declarado": str(origem.motivos),
                       "ameaca_estatal": "nao" if "guerra" not in str(origem.motivos) else "sim", "guerra_no_territorio_12m": "nao", "guerra_no_territorio_24m": "nao",
                       "guerra_no_territorio_60m": "nao" if ano + 5 < 2026 or (ano + 5 == 2026 and data[5:] <= "11") else "aberto", "participou_de_guerra_60m": "", "desastre_grande_60m": "",
                       "houve_sinais_duros": "nao", "sinais_na_data_do_pedido": "nao", "guerra_com_o_ameacante_declarado": "nao", "fonte_1": str(origem.url_oficial), "fonte_2": "", "captura": str(origem.captura),
                       "trecho_curto": str(origem.trecho_curto), "confianca": "media", "observacao": "Entrou na rodada 2 a partir de paises.csv, porque só casos com ameaça estavam na lista; ausência de guerra por conhecimento geral.",
                       "entra_na_taxa": "sim", "motivo_fora": ""})
    e = pd.concat([e, pd.DataFrame(linhas)], ignore_index=True)
    e.to_csv(D / "historia_episodios.csv", index=False)


def paises() -> None:
    p = pd.read_csv(D / "paises.csv", dtype=str)
    p.loc[p.iso3 == "POL", "data_primeira_orientacao"] = "2022"
    p.loc[p.iso3 == "POL", "fonte_data_primeira"] = "a própria captura diz Warszawa, 2022 r. Wydanie I"
    p.loc[p.iso3 == "FIN", "menciona_guerra"] = "sim"
    p.loc[p.iso3 == "FIN", "observacao"] = p.loc[p.iso3 == "FIN", "observacao"] + " Rodada 2: o guia do Ministério de 2024 (yle-finlandia, FI-2024) cita conflito militar."
    p.loc[p.iso3 == "LTU", "menciona_guerra"] = "sim"
    p.loc[p.iso3 == "LTU", "observacao"] = p.loc[p.iso3 == "LTU", "observacao"].fillna("") + " Rodada 2: guia What to do in case of crisis or war em ep-lituania-2024-iidraudimas."
    p.loc[p.iso3 == "CAN", "captura"] = "oficiais/can-2007.txt"
    p.to_csv(D / "paises.csv", index=False)


def interrupcoes() -> None:
    i = pd.read_csv(D / "brasil_interrupcoes_longas.csv", dtype=str)
    i.loc[i.caso == "Enel SP outubro", "pessoas"] = "3,1 milhões de clientes no dia"
    i.to_csv(D / "brasil_interrupcoes_longas.csv", index=False)


if __name__ == "__main__":
    episodios()
    paises()
    interrupcoes()
    print("ok")
