"""Baixa o dado público da etapa E6 para dados/brutos/brasil/ e registra cada arquivo em dados/MANIFESTO_BRASIL.json.

Fontes: ComexStat (API do MDIC), IBGE SIDRA, Banco Central (SGS), ANEEL (dados abertos), ANP (série mensal de preços),
Conab (portal de informações), UN Comtrade (prévia pública) e o arquivo bruto da balança comercial.
Um download por vez, com pausa. Fonte que recusar fica registrada com o erro, e a coleta segue.

Uso: python ferramentas/coletar_brasil.py [grupo ...]
Grupos: comex sidra bcb aneel anp conab comtrade documentos balanca (sem grupo, baixa tudo menos balanca)
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import sys
import time
import urllib.parse
from pathlib import Path

import requests
import urllib3

RAIZ = Path(__file__).resolve().parents[1]
BRUTOS = RAIZ / "dados" / "brutos" / "brasil"
MANIFESTO = RAIZ / "dados" / "MANIFESTO_BRASIL.json"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/129.0 Safari/537.36", "Accept": "*/*"}
PAUSA = 3

ANO_INICIO = 2015
ANO_FIM = 2026  # 2026 parcial: o ComexStat informa o último mês em comex-atualizacao.json

COMEX = "https://api-comexstat.mdic.gov.br/general?language=pt"
SIDRA = "https://apisidra.ibge.gov.br/values/t/{t}/n1/all/v/63,2265/p/{p}/c315/7169,7171"
SGS = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{n}/dados?formato=json&dataInicial=01/01/2018&dataFinal=30/09/2026"
ANEEL_BASE = "https://dadosabertos.aneel.gov.br/dataset/d5f0712e-62f6-4736-8dff-9991f10758a7/resource/"
ANEEL = {
    "aneel-continuidade-2020-2029.zip": ANEEL_BASE + "4493985c-baea-429c-9df5-3030422c71d7/download/indicadores-continuidade-coletivos-2020-2029.zip",
    "aneel-continuidade-2010-2019.zip": ANEEL_BASE + "b4dbdc46-a8a3-4e5d-9565-9f23b1156496/download/indicadores-continuidade-coletivos-2010-2019.zip",
    "aneel-dicionario-continuidade.pdf": ANEEL_BASE + "5d91171a-eb4e-4f66-8418-2833567123ae/download/dm-indicadores-continuidade.pdf",
    "aneel-dominio-indicadores.csv": ANEEL_BASE + "17fc99b7-e707-4ec4-9553-a43d7a41f7a6/download/dominio-indicadores.csv",
}
ANP = {"anp-precos-mensal-brasil-desde-2013.xlsx": "https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/precos-revenda-e-de-distribuicao-combustiveis/shlp/mensal/mensal-brasil-desde-jan2013.xlsx"}
CONAB_PASTA = "https://www.gov.br/conab/pt-br/atuacao/logistica/estoques-publicos/estoques-por-produto/"
# O endereço ficou com o mês antigo no nome, mas a página de listagem (conab-pagina-estoques-publicos.html) mostra
# que o arquivo por trás é o de setembro de 2026, com última modificação em 14/10/2026.
CONAB = {
    "conab-pagina-estoques-publicos.html": CONAB_PASTA + "estoques-por-produto",
    "conab-serie-historica-estoques-set2026.pdf": CONAB_PASTA + "serie-historica-de-estoques-de-produtos-julho-2025.pdf",
    "conab-serie-historica-estoques-uf-set2026": CONAB_PASTA + "serie-historica-de-estoques-de-produtos-junho-2025.pdf",
}
BALANCA = {"balanca-IMP_2024.csv": "https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/IMP_2024.csv"}
COMTRADE = "https://comtradeapi.un.org/public/v1/preview/C/A/HS?reporterCode=76&period={ano}&cmdCode=310210&flowCode=M&partnerCode=&partner2Code=0&customsCode=C00&motCode=0"

# Estes dois servidores do governo não entregam a cadeia completa do certificado.
# Documentos oficiais em PDF citados nas tabelas curadas.
DOCUMENTOS = {
    "doc-tcu-apagao-2023.pdf": "https://agenciainfra.com/blog/wp-content/uploads/2026/03/TCU-Apagao-2023-REPR.pdf",
    "doc-tcu-enel-sp.pdf": "https://agenciainfra.com/blog/wp-content/uploads/2025/12/instrucao-tcu-enel-sp-aneel.pdf",
    "doc-enel-sp-camara-dez2024.pdf": "https://www2.camara.leg.br/atividade-legislativa/comissoes/comissoes-permanentes/cme/apresentacoes-em-eventos/apresentacoes-em-eventos-2024/atuacao-da-enel-no-fornecimento-de-energia-nos-estados-de-sao-paulo-e-do-rio-de-janeiro/ENEL%20SP_%20CME%20DEZ_2024.pdf",
    "doc-sc-plano-emergencial-familiar.pdf": "https://defesacivil.sc.gov.br/wp-content/uploads/2024/06/PLANO-EMERGENCIAL-FAMILIAR.pdf",
    "doc-cemaden-cartilha-desastres.pdf": "https://educacao.cemaden.gov.br/wp-content/uploads/cemaden-educacao/Cartilha_Desastres_3%C2%B0versao_fundo_branco-1.pdf",
}

SEM_VERIFICAR = ("portaldeinformacoes.conab.gov.br", "balanca.economia.gov.br")


def carregar_manifesto() -> dict:
    return json.loads(MANIFESTO.read_text(encoding="utf-8")) if MANIFESTO.exists() else {"arquivos": {}, "falhas": {}}


def registrar(man: dict, nome: str, url: str, corpo_post: dict | None = None) -> None:
    caminho = BRUTOS / nome
    h = hashlib.sha256()
    with caminho.open("rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    entrada = {
        "url": url,
        "hora": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "bytes": caminho.stat().st_size,
        "sha256": h.hexdigest(),
    }
    if corpo_post is not None:
        entrada["corpo_post"] = corpo_post
    man["arquivos"][nome] = entrada
    man["falhas"].pop(nome, None)
    MANIFESTO.write_text(json.dumps(man, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    print(f"ok   {nome}  {entrada['bytes']:,} bytes")


def falhou(man: dict, nome: str, url: str, erro: str) -> None:
    man["falhas"][nome] = {"url": url, "hora": dt.datetime.now().astimezone().isoformat(timespec="seconds"), "erro": erro[:300]}
    MANIFESTO.write_text(json.dumps(man, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    print(f"FALHA {nome}: {erro[:160]}")


def baixar(man: dict, nome: str, url: str, reusar: bool = True) -> None:
    caminho = BRUTOS / nome
    if reusar and caminho.exists() and nome in man["arquivos"]:
        print(f"já tem {nome}")
        return
    verificar = not any(h in url for h in SEM_VERIFICAR)
    try:
        with requests.get(url, headers=UA, timeout=180, stream=True, verify=verificar) as r:
            r.raise_for_status()
            with caminho.open("wb") as f:
                for bloco in r.iter_content(1 << 20):
                    f.write(bloco)
        registrar(man, nome, url)
    except Exception as e:  # fonte que recusa fica registrada, a coleta segue
        caminho.unlink(missing_ok=True)
        falhou(man, nome, url, repr(e))
    time.sleep(PAUSA)


def consulta_comex(man: dict, nome: str, corpo: dict) -> None:
    caminho = BRUTOS / nome
    if caminho.exists() and nome in man["arquivos"]:
        print(f"já tem {nome}")
        return
    for tentativa in range(30):
        try:
            r = requests.post(COMEX, json=corpo, headers={**UA, "Content-Type": "application/json"}, timeout=120)
            if r.status_code == 429:  # a própria API pede 10 segundos
                time.sleep(15)
                continue
            r.raise_for_status()
            d = r.json()
            if not d.get("success", True) and not d.get("data"):
                raise ValueError(str(d)[:200])
            caminho.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
            registrar(man, nome, COMEX, corpo)
            time.sleep(25)
            return
        except Exception as e:
            erro = repr(e)
            time.sleep(10)
    else:
        erro = "429 repetido"
    falhou(man, nome, COMEX, erro)


def comex(man: dict) -> None:
    baixar(man, "comex-atualizacao.json", "https://api-comexstat.mdic.gov.br/general/dates/updated", reusar=False)
    # A API devolve uma linha por ano quando o período cobre vários anos, então cinco consultas bastam.
    periodo = {"from": f"{ANO_INICIO}-01", "to": f"{ANO_FIM}-12"}
    metricas = ["metricFOB", "metricKG"]
    ureia = [{"filter": "ncm", "values": ["31021010"]}]
    consulta_comex(man, "comex-ureia-pais.json", {"flow": "import", "monthDetail": False, "period": periodo, "filters": ureia, "details": ["country"], "metrics": metricas})
    consulta_comex(man, "comex-cap31-pais.json", {"flow": "import", "monthDetail": False, "period": periodo, "filters": [{"filter": "chapter", "values": ["31"]}], "details": ["country"], "metrics": metricas})
    # o outro código de ureia (31021090), para saber quanto fica fora do recorte
    consulta_comex(man, "comex-ureia-outra.json", {"flow": "import", "monthDetail": False, "period": periodo, "filters": [{"filter": "ncm", "values": ["31021090"]}], "details": ["ncm"], "metrics": metricas})
    consulta_comex(man, "comex-ureia-export.json", {"flow": "export", "monthDetail": False, "period": periodo, "filters": ureia, "details": ["ncm"], "metrics": metricas})
    # mês a mês, por país, de 2025 em diante: é o que mostra o que mudou na crise de 2026
    consulta_comex(man, "comex-ureia-pais-mes-2025-2026.json", {"flow": "import", "monthDetail": True, "period": {"from": "2025-01", "to": "2026-12"}, "filters": ureia, "details": ["country"], "metrics": metricas})


def sidra(man: dict) -> None:
    baixar(man, "sidra-1419-ipca-2018-2019.json", SIDRA.format(t=1419, p="201801-201912"))
    baixar(man, "sidra-7060-ipca-2020-2026.json", SIDRA.format(t=7060, p="202001-202612"), reusar=False)


def bcb(man: dict) -> None:
    baixar(man, "bcb-sgs-27864-alimentacao-domicilio.json", SGS.format(n=27864))


def aneel(man: dict) -> None:
    for nome, url in ANEEL.items():
        baixar(man, nome, url)


def anp(man: dict) -> None:
    for nome, url in ANP.items():
        baixar(man, nome, url)


def conab(man: dict) -> None:
    for nome, url in CONAB.items():
        baixar(man, nome, url)


def comtrade(man: dict) -> None:
    for ano in (2022, 2023, 2024, 2025):
        baixar(man, f"comtrade-310210-brasil-{ano}.json", COMTRADE.format(ano=ano))


def documentos(man: dict) -> None:
    for nome, url in DOCUMENTOS.items():
        baixar(man, nome, url)


def balanca(man: dict) -> None:
    for nome, url in BALANCA.items():
        baixar(man, nome, url)


GRUPOS = {"comex": comex, "sidra": sidra, "bcb": bcb, "aneel": aneel, "anp": anp, "conab": conab, "comtrade": comtrade, "documentos": documentos, "balanca": balanca}


def main() -> None:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    BRUTOS.mkdir(parents=True, exist_ok=True)
    man = carregar_manifesto()
    # o arquivo bruto da balança passa de 100 MB e só serviria de conferência extra: só com pedido explícito
    for g in sys.argv[1:] or [x for x in GRUPOS if x != "balanca"]:
        print(f"== {g}")
        GRUPOS[g](man)


if __name__ == "__main__":
    main()
