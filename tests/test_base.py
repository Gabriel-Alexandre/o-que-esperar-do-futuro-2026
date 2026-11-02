import json
from pathlib import Path

import pandas as pd

R = Path(__file__).resolve().parents[1]
D = R / "dados" / "derivados"


def test_estudos_de_caso_fora_da_taxa():
    e = pd.read_csv(D / "historia_episodios.csv", dtype=str).set_index("id")
    for i in ("UA-2021", "IN-2025", "CN-1969", "EU-2025"):
        assert e.loc[i].entra_na_taxa == "nao"


def test_valores_de_guerra():
    e = pd.read_csv(D / "historia_episodios.csv", dtype=str)
    assert set(e.guerra_no_territorio_60m) <= {"sim", "nao", "aberto"}


def test_lista_tem_33():
    p = pd.read_csv(D / "paises.csv", dtype=str)
    assert (p.na_lista_newsweek == "sim").sum() == 33


def test_cenarios_somam_100():
    assert pd.read_csv(R / "resultados" / "cenarios.csv").chance_pct.sum() == 100


def test_resumo_bate_com_cenario():
    r = json.loads((R / "resultados" / "RESUMO.json").read_text(encoding="utf-8"))
    assert r["historia"]["com_sinais_duros"]["60m"]["k"] == 4


def test_trecho_de_video_e_curto():
    a = pd.read_csv(D / "videos_afirmacoes.csv", dtype=str)
    assert a.afirmacao.str.split().str.len().max() <= 25
