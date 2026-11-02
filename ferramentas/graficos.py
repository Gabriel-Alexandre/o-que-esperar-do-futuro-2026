"""Gráficos 1920x1080 a partir de resultados/RESUMO.json e de dados/derivados. Uso: python ferramentas/graficos.py"""
from __future__ import annotations

import json
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
DER = RAIZ / "dados" / "derivados"
FIG = RAIZ / "resultados" / "figuras"
AZUL, OURO, CINZA, TIJOLO, TINTA = "#2F5D8C", "#C9902B", "#8A8A8A", "#C8553D", "#222222"
RODAPE = "github.com/Gabriel-Alexandre/o-que-esperar-do-futuro-2026 · análise feita pelo Claude"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 22, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#BBBBBB", "xtick.color": "#444444", "ytick.color": "#444444"})
R = json.loads((RAIZ / "resultados" / "RESUMO.json").read_text(encoding="utf-8"))


def nova(titulo, sub, **ajuste):
    f, a = plt.subplots(figsize=(16, 9), dpi=120)
    b = dict(left=0.08, right=0.95, top=0.78, bottom=0.16)
    b.update(ajuste)
    f.subplots_adjust(**b)
    f.text(0.05, 0.92, titulo, fontsize=36, fontweight="bold", color=TINTA)
    f.text(0.05, 0.855, sub, fontsize=22, color="#444444")
    return f, a


def salvar(f, nome, fonte):
    f.text(0.05, 0.05, "Fonte: " + fonte, fontsize=15, color="#555555")
    f.text(0.05, 0.018, RODAPE, fontsize=15, color="#555555")
    FIG.mkdir(parents=True, exist_ok=True)
    f.savefig(FIG / f"{nome}.png")
    plt.close(f)


def g01():
    p = pd.read_csv(DER / "paises.csv")
    p = p[(p.na_lista_newsweek == "sim") & p.prazo_max_dias.notna() & (p.abrangencia == "nacional")].sort_values("prazo_max_dias")
    f, a = nova("A maioria pede até 3 dias, e ninguém pede meses", f"Meta máxima em dias nos documentos oficiais de {len(p)} países com prazo nacional", left=0.17, top=0.82, bottom=0.13)
    a.barh(p.pais, p.prazo_max_dias, color=[TIJOLO if m == "sim" else AZUL for m in p.menciona_guerra], height=0.72)
    for i, v in enumerate(p.prazo_max_dias):
        a.text(v + 0.15, i, f"{int(v)}", va="center", fontsize=15, color=TINTA)
    a.tick_params(axis="y", labelsize=14)
    a.text(0.98, 0.25, "vermelho: o documento\ncita guerra\n\nazul: não cita", transform=a.transAxes, ha="right", fontsize=22, color=TINTA)
    a.set_xlabel("dias")
    salvar(f, "g01_prazo_por_pais", "documentos oficiais de cada governo, lidos em 02/nov/2026")


def g02():
    p = pd.read_csv(DER / "paises.csv")
    p = p[p.na_lista_newsweek == "sim"]
    d = p.dropna(subset=["data_primeira_orientacao"]).copy()
    d["ano"] = d.data_primeira_orientacao.astype(str).str[:4].astype(int)
    d = d.sort_values("ano").reset_index(drop=True)
    f, a = nova("Os 33 países não começaram agora", f"Primeira orientação achada: {len(d)} têm data, de 1943 a 2025; {33 - len(d)} ficaram sem data confirmada", left=0.17, top=0.8, bottom=0.14)
    a.scatter(d.ano, range(len(d)), s=150, color=AZUL, zorder=3)
    a.set_yticks(range(len(d)), d.pais, fontsize=15)
    a.set_xscale("function", functions=(lambda x: (x - 1930) ** 2.2, lambda x: x ** (1 / 2.2) + 1930))
    a.set_xticks([1943, 2003, 2018, 2025])
    a.grid(axis="x", color="#E5E5E5")
    a.set_axisbelow(True)
    salvar(f, "g02_primeira_orientacao", "documentos oficiais e imprensa; a escala do tempo é comprimida nos anos antigos")


def g03():
    t = pd.read_csv(RAIZ / "resultados" / "termometro.csv")
    te = R["paises"]["termometro"]
    f, a = nova("O termômetro de guerra é um sinal fraco", f"Dias pedidos e distância da Rússia: correlação {str(te['spearman_todos']).replace('.', ',')}, que não dá para separar do acaso", top=0.8)
    a.scatter(t.km_russia, t.prazo_max_dias, s=170, color=[TIJOLO if m == "sim" else AZUL for m in t.menciona_guerra], zorder=3, edgecolor="white", linewidth=2)
    for nome in ["Japão", "Singapura", "Áustria", "Alemanha", "Argentina"]:
        l = t[t.pais == nome]
        if len(l):
            a.annotate(nome, (l.km_russia.iloc[0], l.prazo_max_dias.iloc[0]), xytext=(10, 8), textcoords="offset points", fontsize=18, color=TINTA)
    a.set_xlabel("distância da capital até território russo (km)")
    a.set_ylabel("dias pedidos")
    a.grid(color="#EEEEEE")
    a.text(0.99, 0.93, "vermelho: cita guerra · azul: não cita", transform=a.transAxes, ha="right", fontsize=19, color=TINTA)
    salvar(f, "g03_termometro", "documentos oficiais; distância até Moscou, São Petersburgo, Kaliningrado ou Vladivostok; o resultado depende de Singapura")


def g04():
    h = R["historia"]
    fx = h["faixa_so_o_pedido_60m"]
    ks = [(k, v) for k, v in fx.items()]
    com = h["com_sinais_duros"]["60m"]
    f, a = nova("Só o pedido quase nunca veio antes de guerra", "Guerra no território em até 5 anos. A faixa muda com a regra; não há grupo sem campanha", left=0.38, top=0.8)
    linhas = [("com evacuação, racionamento, convocação\nou máscara em massa junto", com, TIJOLO)] + [("só o pedido: " + k, v, AZUL) for k, v in ks]
    for i, (n, t, c) in enumerate(reversed(linhas)):
        a.barh(i, t["pct"], color=c, height=0.6)
        a.text(t["pct"] + 1.5, i, f"{t['k']} de {t['n']}", va="center", fontsize=24, fontweight="bold", color=TINTA)
    a.set_yticks(range(len(linhas)), [x[0] for x in reversed(linhas)], fontsize=17)
    a.set_xlim(0, 100)
    a.set_xlabel("% dos episódios")
    salvar(f, "g04_taxa_base", "base própria; amostra por busca, não aleatória; sinais codificados conhecendo o resultado")


def g05():
    s = pd.DataFrame(R["sinais"])
    nomes = {"UK-1939": "Reino Unido, fev/1939", "UK-1980": "Reino Unido, mai/1980", "US-1961": "EUA, set/1961", "UA-2022": "Ucrânia, jan/2022",
             "HOJE-UK": "Reino Unido, hoje", "HOJE-DE": "Alemanha, hoje", "HOJE-PL": "Polônia, hoje", "HOJE-SE": "Suécia, hoje", "HOJE-FI": "Finlândia, hoje",
             "HOJE-TW": "Taiwan, hoje", "HOJE-JP": "Japão, hoje", "HOJE-US": "EUA, hoje"}
    s["nome"] = s.momento.map(nomes)
    ordem = list(nomes.values())[::-1]
    s = s.set_index("nome").loc[ordem].reset_index()
    f, a = nova("Os sinais duros, no que dá para ver", "Pontos em 10 itens. Em cinza, o que está sem dado: dá para comparar pouco com hoje", left=0.25, top=0.8)
    a.barh(s.nome, s.pontos, color=[AZUL if "hoje" in n else TINTA for n in s.nome], height=0.72)
    a.barh(s.nome, s.sem_dado, left=10 - s.sem_dado, color="#E2E2E2", height=0.72)
    for i, (_, l) in enumerate(s.iterrows()):
        a.text(l.pontos + 0.1, i, str(l.pontos).replace(".0", "").replace(".", ","), va="center", fontsize=20, color=TINTA)
    a.set_xlim(0, 10)
    a.tick_params(axis="y", labelsize=18)
    a.set_xlabel("pontos: sim vale 1, parcial vale 0,5")
    salvar(f, "g05_sinais", "base própria; a Ucrânia marcou pouco um mês antes da invasão, então pouco ponto não garante nada")


def g06():
    h = pd.DataFrame(R["hipoteses"]["tabela"])
    nomes = {"H1a_guerra_com_data_sabida": "guerra com data sabida", "H1b_guerra_plausivel_sem_data": "guerra plausível, sem data", "H2_seguro_geral_sem_guerra_em_mente": "seguro geral, sem guerra em mente", "H3_clima_e_desastre": "clima e desastre",
             "H4_ciber_e_ia": "ciberataque e IA", "H5_choque_de_abastecimento": "choque de abastecimento", "H6_copia_entre_governos": "um governo copia o outro", "H7_politica_e_orcamento": "política e orçamento"}
    h["n"] = h.hipotese.map(nomes)
    h = h[::-1]
    f, a = nova("O método derruba a guerra com data, não a plausível", "Peso das evidências contra cada hipótese, por dois codificadores independentes (Heuer)", left=0.34, top=0.8)
    y = range(len(h))
    a.barh([i + 0.19 for i in y], h.contra_1, height=0.36, color=TIJOLO, label="1º codificador")
    a.barh([i - 0.19 for i in y], h.contra_2, height=0.36, color=OURO, label="2º, às cegas")
    a.set_yticks(list(y), h.n, fontsize=20)
    a.legend(frameon=False, fontsize=20, loc="lower right")
    a.set_xlabel("peso contra (alto 2, médio 1, baixo 0,5)")
    salvar(f, "g06_hipoteses", "21 evidências em dados/derivados; as hipóteses podem valer juntas; é julgamento, não medida")


def g07():
    c = pd.read_csv(RAIZ / "resultados" / "cenarios.csv").sort_values("ordem", ascending=False)
    cor = {"A": AZUL, "B": CINZA, "C": OURO, "E": "#7A5C99", "D": TIJOLO}
    f, a = nova("O que esperar até o fim de 2029", "O pior ponto que o mundo alcança. Leitura da IA, com faixa, registrada para ser cobrada", left=0.05, top=0.8)
    for i, (_, l) in enumerate(c.iterrows()):
        a.barh(i, l.chance_pct, color=cor[l.id], height=0.42)
        a.plot([l.faixa_min, l.faixa_max], [i, i], color=TINTA, lw=3)
        a.text(max(l.chance_pct, l.faixa_max) + 1, i, f"cerca de {l.chance_pct}%", va="center", fontsize=28, fontweight="bold", color=TINTA)
        a.text(0, i + 0.3, f"{l.id} · {l.nome}: {l.resumo.replace(';', ',')}", fontsize=21, color=TINTA)
    a.set_xlim(0, 100)
    a.set_ylim(-0.5, len(c) - 0.2)
    a.axis("off")
    salvar(f, "g07_cenarios", "resultados/cenarios.csv; a linha preta é a faixa; julgamento de uma IA, não medida")


def g08():
    r = pd.read_csv(DER / "brasil_fertilizantes_resumo.csv")
    u = r[r.recorte.str.contains("ureia", case=False) & (r.ano >= 2019)]
    f, a = nova("O Brasil depende do Golfo? Depende de como se conta", "Ureia importada por origem. A base dá o país, não o porto; Omã tem fábrica fora do estreito", top=0.8)
    anos = u.ano.astype(str).where(u.ano < 2026, "2026 parcial")
    a.bar(anos, u.fatia_dentro_do_golfo_pct, color=TIJOLO, label="dentro do Golfo", width=0.6)
    a.bar(anos, u.fatia_oma_pct, bottom=u.fatia_dentro_do_golfo_pct, color=OURO, label="Omã", width=0.6)
    for x, g, o in zip(anos, u.fatia_dentro_do_golfo_pct, u.fatia_oma_pct):
        a.text(x, g + o + 0.8, f"{g + o:.0f}%".replace(".", ","), ha="center", fontsize=22, color=TINTA, bbox=dict(fc="white", ec="none", pad=1), zorder=5)
    a.axhline(41, color=TINTA, lw=2, ls="--")
    a.text(7.4, 42, "41%: consultoria, pelo caminho do navio", fontsize=20, color=TINTA, ha="right")
    a.legend(frameon=False, fontsize=20, loc="upper right")
    a.set_ylabel("% das toneladas")
    a.set_ylim(0, 60)
    salvar(f, "g08_ureia_golfo", "ComexStat/MDIC, 2026 de janeiro a setembro; conferido contra o Comtrade")


def g09():
    m = pd.read_csv(DER / "brasil_fertilizantes_mensal.csv")
    m = m[m.mes >= "2025-01"].reset_index(drop=True)
    f, (a, b) = plt.subplots(2, 1, figsize=(16, 9), dpi=120, sharex=True)
    f.subplots_adjust(left=0.08, right=0.95, top=0.78, bottom=0.17, hspace=0.25)
    f.text(0.05, 0.92, "A ureia: o preço voltou, o volume não", fontsize=36, fontweight="bold", color=TINTA)
    f.text(0.05, 0.855, "Importação do Brasil, mês a mês, até setembro. Preço de importação reflete contrato antigo", fontsize=22, color="#444444")
    a.plot(m.mes, m.preco_medio_usd_t, color=AZUL, lw=4)
    a.set_title("dólares por tonelada", loc="left", fontsize=20)
    pico = m.preco_medio_usd_t.idxmax()
    a.annotate(f"US$ {m.preco_medio_usd_t[pico]:.0f}", (pico, m.preco_medio_usd_t[pico]), xytext=(14, -6), textcoords="offset points", fontsize=20)
    a.annotate(f"US$ {m.preco_medio_usd_t.iloc[-1]:.0f}", (len(m) - 1, m.preco_medio_usd_t.iloc[-1]), xytext=(-60, 14), textcoords="offset points", fontsize=20)
    b.bar(m.mes, m.toneladas / 1e3, color=OURO)
    b.set_title("mil toneladas", loc="left", fontsize=20)
    b.set_xticks(range(0, len(m), 3), m.mes[::3], rotation=30, fontsize=15)
    salvar(f, "g09_ureia_preco", "ComexStat/MDIC")


def g10():
    i = pd.read_csv(DER / "brasil_ipca_alimentos.csv")
    i = i[i.mes >= "2019-01"]
    f, a = nova("A comida no Brasil subiu de zero para 4,2% desde a guerra", "Alimentação no domicílio, em 12 meses. A causa não está separada; a S&P vê o efeito do adubo em 2027", top=0.8)
    y = i.alim_dom_12m_pct.fillna(i.alim_dom_12m_recalculado_pct)
    a.plot(i.mes, y, color=TIJOLO, lw=4)
    a.set_xticks(range(0, len(i), 12), i.mes[::12], fontsize=18)
    a.annotate(f"{y.iloc[-1]:.2f}%".replace(".", ","), (len(i) - 1, y.iloc[-1]), xytext=(-60, 22), textcoords="offset points", fontsize=28, fontweight="bold", color=TINTA)
    a.grid(axis="y", color="#EEEEEE")
    a.set_ylabel("%")
    salvar(f, "g10_ipca_alimentos", "IBGE, IPCA, tabelas 1419 e 7060; jan a nov de 2020 encadeados")


def g11():
    c = pd.read_csv(DER / "brasil_interrupcoes_longas.csv").dropna(subset=["dias_sem_servico"]).sort_values("dias_sem_servico")
    f, a = nova("O Brasil já passou de 72 horas, sem nenhum ataque", "Dias nos maiores casos com número. Greve é falta de combustível e comida, não falta total", left=0.3, top=0.8)
    nomes = c.caso + " (" + c.ano.astype(str) + ")"
    a.barh(nomes, c.dias_sem_servico, color=AZUL, height=0.62)
    for i, v in enumerate(c.dias_sem_servico):
        a.text(v + 0.3, i, ("6 horas" if v < 1 else f"{int(v)} dias"), va="center", fontsize=22, color=TINTA, bbox=dict(fc="white", ec="none", pad=1), zorder=5)
    a.axvline(3, color=TIJOLO, lw=3, ls="--")
    a.text(3.2, 0.42, "72 h", fontsize=20, color=TIJOLO)
    a.tick_params(axis="y", labelsize=20)
    salvar(f, "g11_casos_brasil", "dados/derivados/brasil_interrupcoes_longas.csv, cada caso com fonte; nem todos ficaram sem serviço por todos os dias")


def g12():
    v = R["videos"]["por_selo"]
    ordem = [("confirmado", AZUL), ("opiniao", CINZA), ("nao_confirmado", OURO), ("distorcido", TIJOLO), ("falso", "#7A1F12")]
    nomes = {"confirmado": "confirmado", "opiniao": "opinião", "nao_confirmado": "não confirmado", "distorcido": "distorcido", "falso": "falso"}
    f, a = nova("O que estão dizendo nos vídeos", f"{R['videos']['afirmacoes']} afirmações de {R['videos']['videos']} vídeos com cerca de {R['videos']['views_somadas'] / 1e6:.0f} milhões de visualizações".replace(".", ","), left=0.22, top=0.8)
    for i, (k, c) in enumerate(reversed(ordem)):
        a.barh(nomes[k], v.get(k, 0), color=c, height=0.62)
        a.text(v.get(k, 0) + 2, i, str(v.get(k, 0)), va="center", fontsize=26, color=TINTA)
    a.tick_params(axis="y", labelsize=22)
    salvar(f, "g12_o_que_circula", "transcrições de 24 vídeos, classificadas pela IA; não confirmado é falta de captura, não erro do vídeo")


def g13():
    pv = pd.read_csv(RAIZ / "resultados" / "previsoes.csv")
    pv = pv[pv.mercado_mesmo_dia.notna()]
    rot = {"P01": "Ormuz normal em 2026", "P02": "artigo 5 da OTAN em 2026", "P04": "ação russa na UE até 2027", "P05": "China invade Taiwan até 2027"}
    f, a = nova("A IA contra o mercado, no mesmo dia", "Chance em 02/nov/2026. Vai ser medido quando cada prazo vencer", left=0.34, top=0.8)
    for i, (_, l) in enumerate(pv.iterrows()):
        a.plot([l.chance_ia * 100, l.mercado_mesmo_dia * 100], [i, i], color="#CCCCCC", lw=5, zorder=1)
        a.scatter(l.chance_ia * 100, i, s=320, color=AZUL, zorder=3)
        a.scatter(l.mercado_mesmo_dia * 100, i, s=320, color=OURO, zorder=3)
    a.set_yticks(range(len(pv)), [rot[x] for x in pv.id], fontsize=22)
    a.set_ylim(-0.6, len(pv) - 0.4)
    a.set_xlim(0, 25)
    a.set_xlabel("%")
    a.text(0.99, 0.08, "azul: IA · dourado: Polymarket", transform=a.transAxes, ha="right", fontsize=22, color=TINTA)
    a.grid(axis="x", color="#EEEEEE")
    salvar(f, "g13_ia_contra_mercado", "resultados/previsoes.csv e dados/derivados/mercados.csv; o mercado de ação na UE é pequeno")


if __name__ == "__main__":
    for g in (g01, g02, g03, g04, g05, g06, g07, g08, g09, g10, g11, g12, g13):
        g()
    print("ok")
