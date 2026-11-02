"""Refaz os números centrais sem pandas e sem importar analise.py, lendo os CSV linha a linha, e compara com resultados/RESUMO.json."""
from __future__ import annotations

import csv
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DER = RAIZ / "dados" / "derivados"


def ler(n: str) -> list[dict]:
    with (DER / n).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def conta(linhas, coluna):
    fech = [l for l in linhas if l[coluna] in ("sim", "nao")]
    return sum(l[coluna] == "sim" for l in fech), len(fech)


def main() -> None:
    r = json.loads((RAIZ / "resultados" / "RESUMO.json").read_text(encoding="utf-8"))
    ep = [l for l in ler("historia_episodios.csv") if l["entra_na_taxa"] == "sim"]
    pa = [l for l in ler("paises.csv") if l["na_lista_newsweek"] == "sim"]
    vi = ler("videos_afirmacoes.csv")
    com = [l for l in ep if l["sinais_na_data_do_pedido"] == "sim"]
    sem = [l for l in ep if l["sinais_na_data_do_pedido"] == "nao"]
    testes = [
        ("taxa 24m, todos", conta(ep, "guerra_no_territorio_24m"), (r["historia"]["todos"]["24m"]["k"], r["historia"]["todos"]["24m"]["n"])),
        ("taxa 60m, todos", conta(ep, "guerra_no_territorio_60m"), (r["historia"]["todos"]["60m"]["k"], r["historia"]["todos"]["60m"]["n"])),
        ("60m, com sinais", conta(com, "guerra_no_territorio_60m"), (r["historia"]["com_sinais_duros"]["60m"]["k"], r["historia"]["com_sinais_duros"]["60m"]["n"])),
        ("60m, sem sinais", conta(sem, "guerra_no_territorio_60m"), (r["historia"]["sem_sinais_duros"]["60m"]["k"], r["historia"]["sem_sinais_duros"]["60m"]["n"])),
        ("países na lista", len(pa), 33),
        ("documentos com guerra", sum(l["menciona_guerra"] == "sim" for l in pa), r["paises"]["menciona_guerra"]),
        ("afirmações dos vídeos", len(vi), r["videos"]["afirmacoes"]),
        ("guerras sem campanha", len(ler("guerras_sem_campanha.csv")), r["historia"]["guerras_sem_campanha"]),
        ("cenários somam 100", sum(int(l["chance_pct"]) for l in csv.DictReader((RAIZ / "resultados" / "cenarios.csv").open(encoding="utf-8"))), 100),
    ]
    falhas = 0
    linhas = ["| Teste | Refeito | Relatório | Passou |", "|---|---|---|---|"]
    for nome, a, b in testes:
        ok = a == b
        falhas += not ok
        linhas.append(f"| {nome} | {a} | {b} | {'sim' if ok else 'NÃO'} |")
    (RAIZ / "resultados" / "VALIDACAO.md").write_text("# Validação por outro caminho\n\n" + "\n".join(linhas) + "\n", encoding="utf-8")
    print("falhas:", falhas)
    raise SystemExit(1 if falhas else 0)


if __name__ == "__main__":
    main()
