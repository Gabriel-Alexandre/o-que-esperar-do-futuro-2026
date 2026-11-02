# Previsões datadas

**Escritas em 02/nov/2026 pelo Claude, antes de qualquer gráfico e de qualquer resultado futuro.** Ficam aqui para serem medidas com a nota de Brier conforme cada prazo vence. A tabela está em [`resultados/previsoes.csv`](../resultados/previsoes.csv). Nada aqui é recomendação de investimento.

Por que registrar: a melhor referência pública mostra modelos de linguagem atrás dos superprevisores humanos (nota de Brier 0,101 contra 0,081, em ForecastBench, com previsão de empate perto do fim de 2026 e margem larga). Evento raro é difícil para todo mundo. Sem registro, ninguém cobra.

Escala de palavras (ICD 203): quase impossível, até 5% · muito improvável, 5 a 20% · improvável, 20 a 45% · mais ou menos 50/50, 45 a 55% · provável, 55 a 80% · muito provável, 80 a 95% · quase certo, acima de 95%.

## Os cenários até 31/dez/2029

Eles não se somam com as previsões acima: cada caminho é o pior ponto que o mundo alcança no período.

| Cenário | O que acontece | Chance | Sinal que confirmaria |
|---|---|---|---|
| **A · Atrito** | guerras longe, sabotagem e ciberataque com efeito limitado, preço de energia e comida oscilando | 45% (faixa 35 a 55) | Ormuz reabre aos poucos; ataques sem apagão longo; campanhas seguem como guia |
| **B · O ataque que apaga** | ao menos um ataque deixa 1 milhão de pessoas ou mais mais de 72 h sem serviço num país rico, sem guerra direta | 23% (faixa 15 a 30) | ataque com IA contra controlador industrial que para serviço; alerta conjunto novo que cite dano real |
| **C · Choque limitado** | combate declarado entre Rússia e membro da OTAN, com mortos, que para antes de virar guerra geral | 25% (faixa 15 a 35) | drone ou míssil com mortos; artigo 4 repetido; artigo 5 invocado |
| **D · Guerra grande** | grandes potências em combate direto contínuo | 7% (faixa 3 a 12) | os sinais duros: convocação ampla, evacuação planejada, racionamento, famílias de diplomatas saindo |

## De onde vêm os números

| Âncora | Valor | Como pesa |
|---|---|---|
| Campanhas sem sinais duros, guerra no território em 60 meses | 2 de 25, 8% (de 2,2% a 25%) | sobre um país; o mundo tem muitos países, então o cenário fica acima |
| Com sinais duros | 7 de 8, 87,5% | hoje nenhum país chegou lá, e por isso D fica baixo |
| Mercado: ação russa na UE até 2027 | 20,5% (mercado pequeno, US$ 12 mil) | a IA fica abaixo no prazo curto, por causa do que diz a OTAN em 30/ago |
| Inteligência: testes russos em meses (BIS tcheco); OTAN, sem ameaça iminente | as duas são oficiais | puxa C para cima de A em risco e deixa a faixa larga |
| Inteligência dos EUA, mar/2026: China sem plano para 2027 | contra 9,5% do mercado | a IA fica abaixo do mercado |
| Ataques reais (Polônia, usina britânica, água nos EUA) | nenhum deixou 1 milhão por 72 h | B não é o caminho central, e a tendência é de alta |

⚠️ **O que pode fazer a IA errar:** amostra histórica escolhida por busca; sinais codificados conhecendo o resultado; a guerra pode vir sem nenhum sinal público, como nos 13 casos de `guerras_sem_campanha.csv`; e o placar de sinais da Ucrânia em janeiro de 2022 foi baixo (2,5 de 8), um mês antes da invasão.
