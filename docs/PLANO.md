# Plano

**Pergunta:** o que esperar do mundo e do Brasil até 2029, dado que governos estão pedindo à população para ter estoque em casa e o Pentágono está preparando bases para funcionar sem a rede civil?

**O que este projeto não faz:** não diz quando ou se uma guerra começa. Não é recomendação de investimento nem de compra. Quando escrever "espera-se", é uma leitura com faixa de probabilidade, e as previsões ficam registradas em `docs/PREVISOES.md` para serem medidas depois.

## Etapas

| Etapa | O que responde | Método | Saída |
|---|---|---|---|
| E1 | quem pediu o quê, quando e por quê | leitura do documento oficial de cada país | `dados/derivados/paises.csv` |
| E2 | o que veio depois nas outras vezes | classe de referência | `dados/derivados/historia_episodios.csv` |
| E3 | o que governos fazem quando esperam guerra | indicadores e alerta | `dados/derivados/sinais.csv` |
| E4 | por que agora | hipóteses concorrentes (Heuer) | `resultados/hipoteses.csv` |
| E5 | o que esperar | cenários, escala de probabilidade, nota de Brier | `docs/PREVISOES.md`, `resultados/cenarios.csv` |
| E6 | o que muda no Brasil | dado público | `dados/derivados/brasil_*.csv` |
| E7 | o que estão dizendo | afirmação por afirmação | `dados/derivados/videos_afirmacoes.csv` |

Relatório por rodadas: `docs/RODADAS.md`. Só as previsões entram em commit antes de qualquer medição, porque tratam do que ainda não aconteceu.

## Regras de fonte

Duas fontes independentes por fato, documento oficial antes de matéria. Duas datas: a do fato e a da publicação. Número só depois de lido no texto capturado. Texto integral de terceiros fica fora do git; aqui entram o endereço, o hash e um trecho curto.
