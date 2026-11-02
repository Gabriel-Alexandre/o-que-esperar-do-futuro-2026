# Previsões datadas

**Escritas em 02/nov/2026 pelo Claude, depois de medir o passado e antes do futuro.** A primeira versão foi para o git às 10h29 (`3ddc6cd`) com o Brasil às 10h35 (`35a3538`). A revisão adversarial achou contradições, e esta é a emenda 1, do mesmo dia; as duas versões ficam medidas. Tabelas: [`resultados/previsoes.csv`](../resultados/previsoes.csv) e [`resultados/cenarios.csv`](../resultados/cenarios.csv). Nada aqui é recomendação de investimento.

Por que registrar: a melhor referência lida mostra modelos de linguagem atrás dos superprevisores humanos em previsão (nota de Brier 0,101 contra 0,081, ForecastBench), com empate estimado por volta do fim de 2026 e margem larga. Evento raro é difícil para todo mundo. Sem registro, ninguém cobra.

**Escala:** quase nenhuma chance, abaixo de 5% · muito improvável, de 5 a 20% · improvável, 20 a 45% · cerca de 50/50, 45 a 55% · provável, 55 a 80% · muito provável, 80 a 95% · quase certo, acima de 95%. ⚠️ É a escala ICD 203 da inteligência americana, de memória: o PDF oficial recusou a captura.

## Os cenários até 31/dez/2029

Cada caminho é **o pior ponto que o mundo alcança**, na ordem D, E, C, B, A: se dois acontecerem, vale o primeiro da ordem. A resolução de cada um está em `cenarios.csv`. As faixas são opinião e atravessam mais de uma palavra da escala.

| Cenário | O que é | Chance | Faixa |
|---|---|---|---|
| **A · Atrito** | guerras longe, sabotagem e ciberataque com efeito limitado, preço oscilando | cerca de 44% | 34 a 55 |
| **B · O ataque que apaga** | ataque deixa 1 milhão ou mais mais de 72 h sem luz ou água num país da OCDE | cerca de 17% | 8 a 25 |
| **C · Choque limitado** | ataque atribuído à Rússia com mortos em país da OTAN | cerca de 21% | 12 a 30 |
| **E · Guerra grande fora da OTAN ou nuclear** | Taiwan, Coreia, Índia e Paquistão, arma nuclear usada | cerca de 11% | 5 a 18 |
| **D · Guerra grande** | grandes potências em combate direto contínuo | cerca de 7% | 3 a 12 |

**O que é quase certo em qualquer um:** apagão longo por clima ou falha (P07, provável até 2027). As 72 horas vão ser usadas, em geral sem guerra.

## De onde vêm os números

| Âncora | Valor | Como pesa |
|---|---|---|
| Campanhas só com o pedido, guerra no território em 5 anos | de 0% a cerca de 1 em 4, conforme a regra; 2 de 33 na principal (`RESUMO.json`) | sem grupo de comparação; é ponto de partida, não sinal |
| Com sinais duros na data | 4 de 5 | o alcance é curto: das guerras com sinal, a maioria veio em até 12 meses. Pesa até o fim de 2027, depois quase nada |
| Hoje | só a Polônia marca um sinal duro, um programa de abrigos de 2027 a 2031; a Suécia marca grão; muito sem dado | não sustenta D baixo sozinho |
| Choque OTAN e Rússia em 2026 | 12,5% (mercado, US$ 3,5 mi, regra ampla) | é o maior mercado; prazo curto e qualquer uso de força |
| Ação russa na UE até 2027 | 20,5% (mercado, US$ 12 mil) | mercado pequeno, pesa pouco |
| França: ataque de 2030 antecipado para o outono de 2027; Tusk: 7 a 8 meses; BIS tcheco: *"months, not years"* | fontes de governo, capturadas | puxam C para cima |
| Funcionário da OTAN, 30/ago: *"no imminent threat"* via Reuters | "iminente" não fala de 3 anos | pesa só no prazo curto |
| Combate com morte entre Rússia e membro da OTAN | uma vez em cerca de 77 anos (Turquia, 2015; conhecimento geral), 1,3% ao ano | C a 21% em 38 meses é cerca de 7% ao ano, 5 vezes a história. **O argumento para o multiplicador:** a guerra na Ucrânia transborda, e as três fontes acima falam disso. É aposta, e aqui está dita |
| Ataque que apagou 1 milhão por 72 h em país rico | zero em cerca de 16 anos (conhecimento geral); regra de Laplace, 18% em 38 meses | B fica perto disso. A tendência sobe (Polônia, usina britânica, água, IA), e o maior ataque real foi um gerador pequeno |
| Guerra direta de grandes potências desde 1945 | Coreia (conhecimento geral), 3,9% em 38 meses | D fica menos de 2 vezes acima |
| Inteligência dos EUA, mar/2026: China sem plano para 2027 | via Military Times e Fox (`mt-china-2027`, `fox-china-2027`), ⚠️ relatório original recusou a captura; contra 9,5% do mercado | a IA fica abaixo do mercado, e pode estar errada |

**Regra de atualização:** convocação ampla, evacuação planejada ou racionamento em vigor em país da OTAN ou em Taiwan movem D ou E para acima de 20%. Ataque atribuído com mortos resolve C e reabre o resto.

⚠️ **O que pode fazer a IA errar:** amostra histórica escolhida por busca; sinais codificados conhecendo o resultado; a guerra pode vir sem campanha à população encontrada, como nos 13 casos de `guerras_sem_campanha.csv`; o placar da Ucrânia em janeiro de 2022 foi baixo (2,5 de 8), um mês antes da invasão.
