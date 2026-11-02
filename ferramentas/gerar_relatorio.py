"""Escreve RELATORIO.md e RESUMO_SIMPLES.md a partir de resultados/RESUMO.json e das tabelas. Nenhum número à mão."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
R = json.loads((RAIZ / "resultados" / "RESUMO.json").read_text(encoding="utf-8"))
C = pd.read_csv(RAIZ / "resultados" / "cenarios.csv")
P = pd.read_csv(RAIZ / "resultados" / "previsoes.csv")


def n(v) -> str:
    return str(v).replace(".", ",")


def kn(t: dict) -> str:
    return f"{t['k']} de {t['n']} ({n(t['pct'])}%)"


h, p, v, b, hip = R["historia"], R["paises"], R["videos"], R["brasil"], R["hipoteses"]
fx = h["faixa_so_o_pedido_60m"]
te = p["termometro"]
linhas_fx = "\n".join(f"| {k} | {kn(t)} |" for k, t in fx.items())
linhas_hip = "\n".join(f"| {l['hipotese']} | {n(l['contra_1'])} | {n(l['contra_2'])} | {n(l['a_favor_1'])} | {n(l['a_favor_2'])} |" for l in hip["tabela"])
linhas_c = "\n".join(f"| {l.id} · {l.nome} | cerca de {l.chance_pct}% | {l.faixa_min} a {l.faixa_max} | {l.criterio_de_resolucao} | {l.o_que_muda_no_brasil} |" for l in C.sort_values("ordem").itertuples())
linhas_p = "\n".join(f"| {l.id} | {l.pergunta} | {l.prazo} | {n(round(l.chance_ia * 100))}% | {l.palavra_da_escala} | {'' if pd.isna(l.mercado_mesmo_dia) else n(round(l.mercado_mesmo_dia * 100, 1)) + '%'} |" for l in P.itertuples())
linhas_m = "\n".join(f"| {m['pergunta']} | {n(round(m['chance_sim'] * 100, 1))}% | {m['fim']} | US$ {m['volume_usd']:,} |".replace(",", ".") for m in R["mercados"])
sinais = pd.DataFrame(R["sinais"])
linhas_s = "\n".join(f"| {l.momento} | {n(l.pontos)} | {l.de} | {l.sem_dado} |" for l in sinais.itertuples())

Path(RAIZ / "RELATORIO.md").write_text(f"""# O que esperar do futuro: relatório

Gerado por `ferramentas/gerar_relatorio.py`. Análise feita pelo Claude em 02/nov/2026. Dados, regras e revisão neste repositório.

## O que este projeto não consegue dizer

- Quando ou se uma guerra começa. O que há é uma leitura com faixa, registrada para ser cobrada.
- Se campanhas aumentam ou não o risco: **não há grupo de comparação** de países sem campanha.
- A base histórica foi montada por busca, em inglês, e não é uma amostra aleatória. Os sinais duros foram codificados por uma IA que já conhecia o resultado. As margens são o mínimo, e o erro real é maior.
- Cenários e hipóteses são julgamento de IA, e não medida.

## 1. O que é real

- **Os países.** A lista de {p['na_lista']} é uma compilação da Newsweek, com datas diferentes: das {p['com_data_primeira']} com data confirmada, {p['antes_de_2022']} são anteriores a 2022. O prazo mediano é {n(p['mediana_dias'])} dias; {p['ate_3_dias']} pedem até 3 dias e {p['de_7_a_14']} pedem de 7 a 14. A palavra guerra aparece em {p['menciona_guerra']} dos documentos lidos. Por abrangência: {p['por_abrangencia']}.
- **O Pentágono.** O FORTRESS é oficial (memorando de 30/set). Os 90 dias vieram de documentos vistos pela Fox (25/out). Em público: *"30, 60, or even 90 days"* de energia e estoque de 90 dias de peças, combustível e munição (Breaking Defense), e 30 dias em matéria do próprio Pentágono. Sem custo oficial; *"decades"* segundo a Air & Space Forces. É sobre bases, sem nada para casas.
- **O termômetro.** Quanto mais longe da Rússia, menos dias: correlação {n(te['spearman_todos'])}, p = {n(te['p_todos'])}, em {te['n']} países. Não dá para separar do acaso, e depende de Singapura. A palavra guerra separa melhor: mediana de {p['km_mediana_cita_guerra']} km da Rússia em quem cita, {p['km_mediana_nao_cita']} km em quem não cita.

## 2. O que veio depois, nas outras vezes

{h['episodios_na_taxa']} episódios de 1935 a 2025, regra em `docs/REGRA_DE_EPISODIOS.md`. Janela ainda aberta sai do denominador; {h['estudos_de_caso']} ficam como estudos de caso, porque falham a regra de entrada.

| Recorte | 24 meses | 60 meses |
|---|---|---|
| Todos | {kn(h['todos']['24m'])} | {kn(h['todos']['60m'])} |
| Com sinais duros na data | {kn(h['com_sinais_duros']['24m'])} | {kn(h['com_sinais_duros']['60m'])} |
| Só o pedido | {kn(h['sem_sinais_duros']['24m'])} | {kn(h['sem_sinais_duros']['60m'])} |
| Ameaça de outro Estado declarada | {kn(h['ameaca_estatal']['24m'])} | {kn(h['ameaca_estatal']['60m'])} |
| Um voto por país | {kn(h['primeiro_de_cada_pais']['24m'])} | {kn(h['primeiro_de_cada_pais']['60m'])} |
| Depois de 2000 | {kn(h['depois_de_2000']['24m'])} | {kn(h['depois_de_2000']['60m'])} |

Atacado por quem temia, em 60 meses: {kn(h['atacado_por_quem_temia_60m'])}, todos antes de 1991.

**O número que mais depende de escolha**, só o pedido em 60 meses:

| Regra | Resultado |
|---|---|
{linhas_fx}

E o contrário também existe: {h['guerras_sem_campanha']} guerras sem campanha à população encontrada (`guerras_sem_campanha.csv`, sem denominador).

**Leitura:** pedir estoque, sozinho, quase nunca veio antes de guerra. Junto com evacuação, racionamento, convocação ou máscara em massa, veio. O sinal alcança cerca de 12 meses, e campanha nenhuma protege de guerra que venha sem aviso.

## 3. Os sinais de hoje

Pontos: sim 1, parcial 0,5, em 10 itens.

| Momento | Pontos | Itens com dado | Sem dado |
|---|---|---|---|
{linhas_s}

⚠️ Com tanto `sem_dado`, comparar é frágil. A Ucrânia em janeiro de 2022 marcou 2,5 um mês antes da invasão. Pouco ponto não garante nada.

## 4. Por que agora

Heuer: conta o que pesa **contra**. Dois codificadores independentes, com {n(hip['pct_iguais'])}% de células iguais ({hip['celulas_iguais']} de {hip['celulas']}).

| Hipótese | Contra (1º) | Contra (2º) | A favor (1º) | A favor (2º) |
|---|---|---|---|---|
{linhas_hip}

**Leitura:** o método derruba a guerra com data sabida e reduz o choque de abastecimento como motor das campanhas. **Não derruba** a guerra plausível sem data, ciberataque e IA, clima, cópia entre governos. Elas podem valer juntas. Seguro geral sem guerra em mente perde peso onde o documento e o ministro falam em guerra.

## 5. O que esperar até 31/dez/2029

| Cenário | Chance | Faixa | Como resolver | No Brasil |
|---|---|---|---|---|
{linhas_c}

Âncoras e limites: `docs/PREVISOES.md`.

## 6. Previsões datadas

| Id | Pergunta | Prazo | IA | Escala | Mercado no dia |
|---|---|---|---|---|---|
{linhas_p}

Mercados do dia:

| Pergunta | Chance | Fim | Volume |
|---|---|---|---|
{linhas_m}

## 7. O Brasil

- **Campanha nacional:** não achei. ⚠️ A busca do MIDR não foi legível, e o Plano Nacional não foi lido. Há orientações estaduais (`brasil_orientacao_oficial.md`).
- **Ureia:** em 2025, {n(b['golfo_2025_pct'])}% de dentro do Golfo e {n(b['oma_2025_pct'])}% de Omã, contra os 41% de uma consultoria, que conta o caminho do navio. A base oficial dá o país, não o porto. Em 2026, até setembro, {n(b['golfo_2026_pct'])}% e {n(b['oma_2026_pct'])}%.
- **Preço e volume:** US$ {n(b['preco_pico_usd'])} em {b['preco_pico_mes']}, US$ {n(b['preco_ultimo_usd'])} em {b['preco_ultimo_mes']}. As toneladas caíram 21% de janeiro a setembro contra 2025.
- **Comida:** {n(b['alimentos_12m_ultimo_pct'])}% em 12 meses em {b['alimentos_ultimo_mes']}, contra {n(b['alimentos_fev_2026_pct'])}% em fevereiro. A causa não está separada.
- **Falta de serviço:** dos {b['casos']} grandes casos da tabela, {b['casos_com_ataque']} foram ataque, e o maior durou {round(b['maior_dias'])} dias (`brasil_interrupcoes_longas.csv`).

## 8. O que estão dizendo

{v['afirmacoes']} afirmações de {v['videos']} vídeos, somando cerca de {round(v['views_somadas'] / 1e6)} milhões de visualizações. Selos: {v['por_selo']}. {v['vendem_algo']} vendem algo. `nao_confirmado` é falta de captura, e não erro do vídeo. Só paráfrase em `videos_afirmacoes.csv`.

## 9. Validação e revisão

Números centrais refeitos por outro caminho: `resultados/VALIDACAO.md`. Coerência: `ferramentas/conferir_cenarios.py`. Revisão adversarial e o que mudou por ela: `docs/REVISAO_ADVERSARIAL.md` e `docs/RODADAS.md`.
""", encoding="utf-8")

Path(RAIZ / "RESUMO_SIMPLES.md").write_text(f"""# O que esperar do futuro, em português simples

**A pergunta:** governos pedem comida e água em casa e o Pentágono prepara bases para funcionar sem a rede civil. A guerra está chegando? O que esperar?

| O que se pergunta | O que a análise achou | Por quê |
|---|---|---|
| É verdade que tantos países pediram? | sim, mas não agora e não juntos | a lista de {p['na_lista']} é uma compilação; {p['antes_de_2022']} das {p['com_data_primeira']} com data são anteriores a 2022 |
| É por guerra? | em parte: {p['menciona_guerra']} documentos citam guerra | a maioria cita clima e falha de serviço |
| O Pentágono vai ficar 90 dias sem energia? | é meta, e o número varia | 90 na Fox; 30, 60 ou 90 no palco; 30 na matéria oficial; sem custo; pode levar décadas |
| Nas outras vezes que pediram, veio guerra? | só o pedido, quase nunca | {kn(fx['regra principal'])}, e de 0% a {n(fx['estudos de caso e um voto por país']['pct'])}% conforme a regra |
| E quando veio junto com evacuação e racionamento? | quase sempre | {kn(h['com_sinais_duros']['60m'])}, com alcance de cerca de 1 ano |
| Os governos sabem de uma data? | a evidência pesa contra | {n(hip['tabela'][0]['contra_1'])} e {n(hip['tabela'][0]['contra_2'])} de peso contra, nos 2 codificadores |
| Acham guerra possível? | sim, e o método não derruba | chefes de inteligência europeus dizem *"meses, não anos"*; Reino Unido fala em 1.000 dias |
| E a IA nisso? | está dos dois lados | a NSA relatou ataque com script feito por IA contra energia e água; e a IA é quem faz esta análise, abaixo dos melhores humanos em previsão |
| O Brasil? | o risco medido é outro | {b['casos_com_ataque']} ataques em {b['casos']} grandes casos; {round(b['maior_dias'])} dias no Amapá; comida em {n(b['alimentos_12m_ultimo_pct'])}% em 12 meses |

**O que esperar até 2029, na leitura da IA:**

| Cenário | Chance |
|---|---|
{chr(10).join(f"| {l.nome} | cerca de {l.chance_pct}% |" for l in C.sort_values("ordem").itertuples())}

**O que pode fazer errar:** base escolhida por busca, sinais codificados sabendo o resultado, sem grupo de comparação, e a guerra pode vir sem aviso. As {len(P)} previsões ficam em `resultados/previsoes.csv`, para serem cobradas.
""", encoding="utf-8")
print("ok")
