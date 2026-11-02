"""Fotografia dos mercados de previsão do dia, para comparar com as previsões da IA.

Grava a resposta bruta em dados/brutos/mercados/AAAA-MM-DD/ (fora do git), com sha256 em dados/MANIFESTO_MERCADOS.json,
e a tabela leve em dados/derivados/mercados.csv: só mercados ainda abertos, com volume acima do piso.
Preço de mercado é aposta de quem participa, não avaliação de governo; serve de comparação.
Uso: python ferramentas/coletar_mercados.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import time
import urllib.parse
import urllib.request
from datetime import date, datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
BUSCAS = ["russia nato", "russia invade", "world war", "nato article 5", "china taiwan", "taiwan invade", "iran ceasefire",
          "strait of hormuz", "nuclear weapon", "oil price", "cyberattack", "blackout", "us iran"]
PISO_VOLUME = 5000


def main() -> None:
    hoje = date.today().isoformat()
    pasta = RAIZ / "dados" / "brutos" / "mercados" / hoje
    pasta.mkdir(parents=True, exist_ok=True)
    manifesto, linhas, vistos = [], [], set()
    for busca in BUSCAS:
        url = "https://gamma-api.polymarket.com/public-search?" + urllib.parse.urlencode(
            {"q": busca, "limit_per_type": 25, "events_status": "active"})
        corpo = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=40).read()
        arq = pasta / (busca.replace(" ", "_") + ".json")
        arq.write_bytes(corpo)
        manifesto.append({"url": url, "arquivo": str(arq.relative_to(RAIZ)).replace("\\", "/"), "hora": datetime.now().astimezone().isoformat(timespec="seconds"),
                          "sha256": hashlib.sha256(corpo).hexdigest(), "bytes": len(corpo)})
        for ev in json.loads(corpo).get("events") or []:
            for m in ev.get("markets") or []:
                fim = (m.get("endDate") or "")[:10]
                if m.get("id") in vistos or not fim or fim < hoje or m.get("closed"):
                    continue
                vol = float(m.get("volume") or 0)
                if vol < PISO_VOLUME:
                    continue
                try:
                    sim = float(json.loads(m.get("outcomePrices") or "[]")[0])
                except (ValueError, IndexError):
                    continue
                vistos.add(m.get("id"))
                linhas.append({"busca": busca, "pergunta": m.get("question"), "chance_sim": round(sim, 4), "fim": fim,
                               "volume_usd": int(vol), "evento": ev.get("title"), "data_foto": hoje})
        time.sleep(1)
    linhas.sort(key=lambda x: (x["busca"], x["fim"]))
    saida = RAIZ / "dados" / "derivados" / "mercados.csv"
    with saida.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)
    (RAIZ / "dados" / "MANIFESTO_MERCADOS.json").write_text(json.dumps(manifesto, ensure_ascii=False, indent=2), encoding="utf-8")
    print(len(linhas), "mercados")


if __name__ == "__main__":
    main()
