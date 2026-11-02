# O que esperar do futuro: relatório

Gerado por `ferramentas/gerar_relatorio.py`. Análise feita pelo Claude em 02/nov/2026. Dados, regras e revisão neste repositório.

## O que este projeto não consegue dizer

- Quando ou se uma guerra começa. O que há é uma leitura com faixa, registrada para ser cobrada.
- Se campanhas aumentam ou não o risco: **não há grupo de comparação** de países sem campanha.
- A base histórica foi montada por busca, em inglês, e não é uma amostra aleatória. Os sinais duros foram codificados por uma IA que já conhecia o resultado. As margens são o mínimo, e o erro real é maior.
- Cenários e hipóteses são julgamento de IA, e não medida.

## 1. O que é real

- **Os países.** A lista de 33 é uma compilação da Newsweek, com datas diferentes: das 17 com data confirmada, 9 são anteriores a 2022. O prazo mediano é 3,0 dias; 16 pedem até 3 dias e 11 pedem de 7 a 14. A palavra guerra aparece em 12 dos documentos lidos. Por abrangência: {'nacional': 25, 'sem_prazo': 5, 'regional': 2, 'sem_campanha': 1}.
- **O Pentágono.** O FORTRESS é oficial (memorando de 30/set). Os 90 dias vieram de documentos vistos pela Fox (25/out). Em público: *"30, 60, or even 90 days"* de energia e estoque de 90 dias de peças, combustível e munição (Breaking Defense), e 30 dias em matéria do próprio Pentágono. Sem custo oficial; *"decades"* segundo a Air & Space Forces. É sobre bases, sem nada para casas.
- **O termômetro.** Quanto mais longe da Rússia, menos dias: correlação -0,3, p = 0,139, em 26 países. Não dá para separar do acaso, e depende de Singapura. A palavra guerra separa melhor: mediana de 530 km da Rússia em quem cita, 2534 km em quem não cita.

## 2. O que veio depois, nas outras vezes

51 episódios de 1935 a 2025, regra em `docs/REGRA_DE_EPISODIOS.md`. Janela ainda aberta sai do denominador; ['UA-2021', 'CN-1969', 'IN-2025'] ficam como estudos de caso, porque falham a regra de entrada.

| Recorte | 24 meses | 60 meses |
|---|---|---|
| Todos | 5 de 46 (10,9%) | 6 de 38 (15,8%) |
| Com sinais duros na data | 3 de 5 (60,0%) | 4 de 5 (80,0%) |
| Só o pedido | 2 de 41 (4,9%) | 2 de 33 (6,1%) |
| Ameaça de outro Estado declarada | 5 de 28 (17,9%) | 6 de 24 (25,0%) |
| Um voto por país | 3 de 21 (14,3%) | 4 de 19 (21,1%) |
| Depois de 2000 | 0 de 25 (0,0%) | 0 de 17 (0,0%) |

Atacado por quem temia, em 60 meses: 3 de 38 (7,9%), todos antes de 1991.

**O número que mais depende de escolha**, só o pedido em 60 meses:

| Regra | Resultado |
|---|---|
| sem iniciadores nem Malvinas | 0 de 31 (0,0%) |
| regra principal | 2 de 33 (6,1%) |
| um voto por país | 2 de 18 (11,1%) |
| contando os 3 estudos de caso | 5 de 36 (13,9%) |
| estudos de caso e um voto por país | 5 de 21 (23,8%) |

E o contrário também existe: 13 guerras sem campanha à população encontrada (`guerras_sem_campanha.csv`, sem denominador).

**Leitura:** pedir estoque, sozinho, quase nunca veio antes de guerra. Junto com evacuação, racionamento, convocação ou máscara em massa, veio. O sinal alcança cerca de 12 meses, e campanha nenhuma protege de guerra que venha sem aviso.

## 3. Os sinais de hoje

Pontos: sim 1, parcial 0,5, em 10 itens.

| Momento | Pontos | Itens com dado | Sem dado |
|---|---|---|---|
| HOJE-DE | 2,5 | 7 | 3 |
| HOJE-FI | 1,5 | 4 | 6 |
| HOJE-JP | 1,0 | 3 | 7 |
| HOJE-PL | 2,5 | 6 | 4 |
| HOJE-SE | 2,5 | 5 | 5 |
| HOJE-TW | 2,0 | 6 | 4 |
| HOJE-UK | 0,5 | 4 | 6 |
| HOJE-US | 0,0 | 2 | 8 |
| UA-2022 | 2,5 | 8 | 2 |
| UK-1939 | 6,0 | 9 | 1 |
| UK-1980 | 2,0 | 5 | 5 |
| US-1961 | 1,5 | 5 | 5 |

⚠️ Com tanto `sem_dado`, comparar é frágil. A Ucrânia em janeiro de 2022 marcou 2,5 um mês antes da invasão. Pouco ponto não garante nada.

## 4. Por que agora

Heuer: conta o que pesa **contra**. Dois codificadores independentes, com 78,0% de células iguais (131 de 168).

| Hipótese | Contra (1º) | Contra (2º) | A favor (1º) | A favor (2º) |
|---|---|---|---|---|
| H1a_guerra_com_data_sabida | 14,5 | 11,0 | 2,0 | 2,0 |
| H5_choque_de_abastecimento | 5,0 | 2,0 | 2,0 | 3,0 |
| H2_seguro_geral_sem_guerra_em_mente | 4,0 | 2,0 | 7,5 | 13,5 |
| H1b_guerra_plausivel_sem_data | 0,0 | 0,0 | 12,0 | 13,0 |
| H3_clima_e_desastre | 0,0 | 0,0 | 6,5 | 6,0 |
| H4_ciber_e_ia | 0,0 | 0,0 | 11,5 | 9,0 |
| H6_copia_entre_governos | 0,0 | 0,0 | 6,5 | 3,0 |
| H7_politica_e_orcamento | 0,0 | 0,0 | 5,5 | 0,5 |

**Leitura:** o método derruba a guerra com data sabida e reduz o choque de abastecimento como motor das campanhas. **Não derruba** a guerra plausível sem data, ciberataque e IA, clima, cópia entre governos. Elas podem valer juntas. Seguro geral sem guerra em mente perde peso onde o documento e o ministro falam em guerra.

## 5. O que esperar até 31/dez/2029

| Cenário | Chance | Faixa | Como resolver | No Brasil |
|---|---|---|---|---|
| A · Atrito | cerca de 44% | 34 a 55 | nenhum dos outros até 31/dez/2029 | o que o Brasil já vive: apagão por temporal; seca; preço de comida e diesel |
| B · O ataque que apaga | cerca de 17% | 8 a 25 | ataque atribuído pela autoridade deixa 1 milhão ou mais de pessoas sem luz ou água por mais de 72 h em país da OCDE; sem C; E ou D | alerta para as distribuidoras daqui; o risco brasileiro segue sendo falha e clima |
| C · Choque limitado | cerca de 21% | 12 a 30 | ataque atribuído à Rússia pelo governo do país com ao menos 1 morto em território de membro; sem D | bolsa e dólar reagem; comida e adubo mais caros por meses |
| E · Guerra grande fora da OTAN ou arma nuclear | cerca de 11% | 5 a 18 | invasão ou bloqueio com tiro em Taiwan; guerra aberta na Coreia ou entre Índia e Paquistão por mais de 30 dias; ou arma nuclear usada em ataque | comércio com a Ásia e chips; comida e adubo mais caros |
| D · Guerra grande | cerca de 7% | 3 a 12 | combate direto declarado por mais de 30 dias entre EUA; China; Rússia ou OTAN contra uma delas (duas agências) | choque de preço e de comércio; o Brasil fica longe do combate e perto da conta |

Âncoras e limites: `docs/PREVISOES.md`.

## 6. Previsões datadas

| Id | Pergunta | Prazo | IA | Escala | Mercado no dia |
|---|---|---|---|---|---|
| P01 | O tráfego em Ormuz volta ao normal | 2026-12-31 | 10% | muito improvável | 11,5% |
| P02 | Algum membro invoca o artigo 5 da OTAN | 2026-12-31 | 3% | quase nenhuma chance | 4,0% |
| P03 | Rússia invade país da OTAN | 2027-12-31 | 5% | muito improvável |  |
| P04 | Ação militar russa contra país da UE | 2027-12-31 | 15% | muito improvável | 20,5% |
| P05 | China invade Taiwan | 2027-12-31 | 4% | quase nenhuma chance | 9,5% |
| P06 | Ataque (cibernético ou sabotagem) deixa 1 milhão de pessoas ou mais sem luz ou água por mais de 72 horas num país da OCDE | 2027-12-31 | 10% | muito improvável |  |
| P07 | Clima ou falha técnica deixa 1 milhão de pessoas ou mais sem luz ou água por mais de 72 horas num país da OCDE | 2027-12-31 | 70% | provável |  |
| P08 | Governo de país do G20 que hoje não tem campanha nacional lança campanha pedindo estoque doméstico com número de dias | 2027-12-31 | 60% | provável |  |
| P09 | Reino Unido aumenta o pedido de 3 dias para 7 dias ou mais | 2027-12-31 | 10% | muito improvável |  |
| P10 | Pentágono publica documento oficial com 90 dias de energia para todas as grandes bases | 2027-12-31 | 25% | improvável |  |
| P11 | Governo dos Cinco Olhos atribui oficialmente a ataque com uso de IA uma interrupção real de serviço de energia ou água ocorrida depois de 02/nov/2026 | 2027-12-31 | 40% | improvável |  |
| P12 | Ataque atribuído à Rússia pelo governo do país mata ao menos 1 pessoa em território de membro da OTAN | 2029-12-31 | 25% | improvável |  |
| P13 | Guerra direta e contínua entre grandes potências (EUA; China; Rússia; ou OTAN contra uma delas) por mais de 30 dias | 2029-12-31 | 7% | muito improvável |  |
| P14 | Governo federal do Brasil lança campanha nacional pedindo estoque doméstico com número de dias | 2027-12-31 | 5% | muito improvável |  |
| P15 | IPCA de alimentação no domicílio chega a 8% ou mais em 12 meses em algum mês de 2027 | 2027-12-31 | 35% | improvável |  |
| P16 | Evento no Brasil deixa ao menos 100 mil pessoas 7 dias ou mais sem luz ou água | 2029-12-31 | 60% | provável |  |
| P17 | Autoridade brasileira atribui a ataque um apagão que atinja ao menos 100 mil pessoas | 2029-12-31 | 5% | muito improvável |  |

Mercados do dia:

| Pergunta | Chance | Fim | Volume |
|---|---|---|---|
| Will China invade Taiwan by December 31. 2027? | 9.5% | 2028-01-01 | US$ 3.579.983 |
| NATO article 5 before 2027? | 4.0% | 2027-01-01 | US$ 304.062 |
| NATO x Russia military clash by December 31. 2026? | 12.5% | 2027-01-01 | US$ 3.542.763 |
| Will Russia invade a NATO country by December 31. 2026? | 3.1% | 2027-01-01 | US$ 473.853 |
| Russia military action against an EU country by December 31. 2026? | 5.5% | 2027-01-01 | US$ 269.728 |
| Russia military action against an EU country by December 31. 2027? | 20.5% | 2028-01-01 | US$ 12.020 |
| Will Strait of Hormuz traffic not return to normal in 2026? | 88.5% | 2027-02-01 | US$ 429.020 |
| US x Russia military clash by December 31. 2026? | 3.9% | 2027-01-01 | US$ 1.087.939 |

## 7. O Brasil

- **Campanha nacional:** não achei. ⚠️ A busca do MIDR não foi legível, e o Plano Nacional não foi lido. Há orientações estaduais (`brasil_orientacao_oficial.md`).
- **Ureia:** em 2025, 19,84% de dentro do Golfo e 15,56% de Omã, contra os 41% de uma consultoria, que conta o caminho do navio. A base oficial dá o país, não o porto. Em 2026, até setembro, 12,37% e 11,96%.
- **Preço e volume:** US$ 585,9 em 2026-06, US$ 406,2 em 2026-09. As toneladas caíram 21% de janeiro a setembro contra 2025.
- **Comida:** 4,21% em 12 meses em 2026-09, contra -0,09% em fevereiro. A causa não está separada.
- **Falta de serviço:** dos 10 grandes casos da tabela, 0 foram ataque, e o maior durou 22 dias (`brasil_interrupcoes_longas.csv`).

## 8. O que estão dizendo

283 afirmações de 24 vídeos, somando cerca de 12 milhões de visualizações. Selos: {'confirmado': 140, 'opiniao': 60, 'nao_confirmado': 53, 'distorcido': 27, 'falso': 3}. 3 vendem algo. `nao_confirmado` é falta de captura, e não erro do vídeo. Só paráfrase em `videos_afirmacoes.csv`.

## 9. Validação e revisão

Números centrais refeitos por outro caminho: `resultados/VALIDACAO.md`. Coerência: `ferramentas/conferir_cenarios.py`. Revisão adversarial e o que mudou por ela: `docs/REVISAO_ADVERSARIAL.md` e `docs/RODADAS.md`.
