# O que esperar do futuro

Governos estão pedindo à população que tenha estoque em casa, e o Pentágono está preparando bases para funcionar sem a rede civil. Este projeto coloca a IA para estudar história e geopolítica, com métodos conhecidos, e dizer o que esperar do mundo e do Brasil até 2029.

**Não é previsão de data de guerra, nem recomendação de investimento ou de compra.** Análise feita pelo Claude.

Comece por [`RESUMO_SIMPLES.md`](RESUMO_SIMPLES.md), depois [`RELATORIO.md`](RELATORIO.md), [`docs/LEITURA_DA_IA.md`](docs/LEITURA_DA_IA.md) e [`docs/PREVISOES.md`](docs/PREVISOES.md).

## Refazer

```bash
pip install -r requirements.txt
python ferramentas/coletar_mercados.py        # muda a cada dia
python ferramentas/coletar_brasil.py
python ferramentas/derivar_brasil.py
python ferramentas/analise.py
python ferramentas/validacao_independente.py
python ferramentas/conferir_cenarios.py
python ferramentas/graficos.py
python ferramentas/gerar_relatorio.py
python ferramentas/conferir_linguagem.py
python -m pytest -q
```

`paises.csv`, `historia_episodios.csv`, `sinais.csv` e `videos_afirmacoes.csv` são leitura de fontes, com endereço e trecho curto por linha. O texto integral de terceiros não fica no repositório.
