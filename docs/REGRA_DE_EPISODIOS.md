# Regra de episódios (E2) e checklist de sinais (E3)

Escrita em 02/nov/2026, **antes** de codificar qualquer resultado. Mudança depois disto entra como emenda datada no fim, sem apagar o texto original.

## 1. O que conta como episódio

Um episódio entra na lista se cumprir as quatro condições:

1. **Governo nacional.** Governo central, ministério ou agência federal (ou a União Europeia, marcada à parte). Prefeitura, estado, província e ONG ficam fora, salvo programa nacional executado por eles.
2. **Pedido à população em geral.** Folheto, transmissão, site oficial, lei ou campanha dirigida a todas as casas ou a qualquer morador. Pedido só a militares, servidores, empresas ou a uma região de risco natural fica fora.
3. **Ação doméstica concreta.** Estocar comida ou água, montar kit, preparar ou construir abrigo, guardar máscara, tampar janela, preparar plano de família. Só "fique atento" ou "confie no governo" fica fora.
4. **Entre janeiro de 1935 e dezembro de 2025.** Episódio de 2026 fica fora da taxa e pode aparecer como "em aberto", sem entrar em numerador nem denominador.

**O que é um episódio separado:** nova campanha, novo folheto ou nova rodada com data própria no mesmo país. Reedição na mesma campanha conta uma vez. Como rodadas do mesmo país não são independentes, a taxa é informada também **por país** (só o primeiro episódio de cada país).

**Motivo não é critério de entrada.** Episódios por terrorismo, desastre natural, bug de computador ou "todos os perigos" entram, com `motivo_declarado` e `ameaca_estatal` preenchidos, porque são os casos sem guerra depois que a lista precisa ter. A taxa é informada para todos e para o subgrupo `ameaca_estatal=sim`.

**Depois de iniciada a guerra:** pedido feito com a guerra já em curso no próprio território não entra, porque não há "depois" para medir. Fica anotado em `observacao` se aparecer.

**Busca de propósito contra o viés:** procurar fora do Ocidente e procurar casos em que nada aconteceu. A seleção não olha o resultado: o candidato entra ou sai pelas quatro condições, antes de eu checar o que veio depois.

## 2. Definição das colunas de resultado

Contagem a partir do mês do episódio, inclusive o mês seguinte como mês 1.

- **`guerra_no_territorio_12m`, `_24m`, `_60m`:** houve, dentro da janela, combate armado **interestatal** ou **bombardeio por outro Estado** em território internacionalmente reconhecido ou efetivamente controlado pelo país. Foguete de grupo não estatal não conta como interestatal, salvo Estado reconhecidamente lançando; isso fica em `observacao`. Incidente único de fronteira sem bombardeio e com menos de 25 mortos em combate no ano não conta (limiar do UCDP para conflito armado). Guerra civil e terrorismo não contam. Valores: `sim`, `nao`, `aberto` (janela ainda não terminou em 02/nov/2026).
- **`participou_de_guerra_60m`:** o país lutou em guerra interestatal fora do próprio território dentro de 60 meses (limiar de 25 mortos em combate/ano, inclusive coalizão). Mesmos valores.
- **`desastre_grande_60m`:** dentro de 60 meses, desastre natural ou técnico nacional com pelo menos 1.000 mortos no país, ou atentado com pelo menos 100 mortos, ou pandemia declarada. Mesmos valores. Serve para ver se a preparação encontrou outra utilidade.
- **`houve_sinais_duros`:** `sim` se, **junto** com o pedido (mesmo período de cerca de 12 meses), havia evacuação planejada ou em curso, racionamento, convocação ampla ou distribuição de máscara/abrigo em massa. Senão `nao`.
- **`ameaca_estatal`:** `sim` se o documento ou o governo citam ataque de outro Estado (nomeado ou genérico "guerra"); `parcial` se aparece entre outras ameaças; `nao` caso contrário.
- **`confianca`:** `alta` com 2 fontes lidas, sendo pelo menos uma primária ou acadêmica; `media` com 2 fontes lidas secundárias; `baixa` com uma fonte só.
- **Resultado em aberto:** a linha com `aberto` sai do denominador daquela janela. Nunca é contada como `nao`.

## 3. Lista separada: guerras sem campanha

`dados/derivados/guerras_sem_campanha.csv` mede o outro lado: de 10 a 15 países atacados ou em guerra interestatal no próprio território sem pedido nacional à população nos 24 meses anteriores que cumprisse as condições acima. Serve para ler se campanha é sinal: se a maioria das guerras vem sem campanha, a campanha não é condição; a pergunta passa a ser quanto ela aumenta a chance. "Sem campanha" é ausência de achado em busca, então a confiança é sempre menor que a de um episódio positivo, e isso fica escrito.

## 4. Checklist de sinais (E3), fixada antes de pontuar

Os dez sinais que governos dão quando esperam guerra de verdade:

1. Evacuação planejada de civis
2. Racionamento ou lei de abastecimento ativada
3. Convocação ou mobilização ampla
4. Retirada de famílias de diplomatas ou aviso para sair do país
5. Distribuição em massa de máscara ou iodo, ou construção de abrigos públicos
6. Compra pública emergencial de grão e combustível
7. Salto de gasto militar acima de 2 pontos do PIB em 2 anos
8. Lei de poderes de emergência
9. Pré-posicionamento de hospitais e sangue
10. Mudança de sede do governo

**Valores:** `sim` (em curso, ou plano ativo já executado), `parcial` (plano no papel, lei aprovada e não acionada, ou sinal só parte do caminho), `nao` (buscado e não achado ou fonte diz que não), `sem_dado` (não consegui fonte lida). `sem_dado` nunca vira `nao`.

**Momentos:** Reino Unido fev/1939; EUA set/1961; Reino Unido mai/1980; Ucrânia jan/2022; hoje (out/nov 2026) em Reino Unido, Alemanha, Polônia, Suécia, Finlândia, EUA, Japão, Taiwan.

**Placar:** `sim` vale 1, `parcial` vale 0,5, `nao` vale 0, `sem_dado` sai do denominador.

## 5. Registro da aplicação (02/nov/2026, depois de codificar)

**O que ficou fora, e por quê (regra acima, sem olhar resultado depois de escrita):**

| Candidato | Motivo |
|---|---|
| Reino Unido 1963 (Handbook 10) | Hansard: manual de treinamento das defesas civis, vendido por 9 pence, não dirigido ao morador. Falha a condição 2 |
| Suécia 1987 | Fontes em conflito; artigo de Conversation diz que a última distribuição à população foi em 1961. Falha a condição 2 |
| EUA 2017 (Havaí, Guam) | Governo estadual. Falha a condição 1 |
| Coreia do Sul 2017 e 2023 | Exercício de sirene, sem ação em casa. Falha a condição 3 |
| Finlândia 2018 (72 tuntia) | Recomendação de autoridades e da ONG SPEK, sem data e sem emissor nacional claros na fonte lida |
| Austrália 1939 e 1941 | Captura falhou; o que apareceu em busca é de governo estadual (Victoria) |
| Japão 2013 | Nenhuma fonte lida |
| Reino Unido 1999 (Y2K), Nova Zelândia 1999 | Só relato indireto; o trecho lido da Nova Zelândia cita chefes de defesa civil e o resto da matéria é pago |
| Ucrânia decreto nacional 2021 | Não achado: UA-2021 entra por vice-prefeito de Kyiv e órgãos públicos, marcado em observação |

**Emendas aplicadas:**

1. Janela com o evento já ocorrido vale `sim` mesmo que a janela não tenha terminado (UA-2021 em 60 meses). `aberto` só quando nada ocorreu ainda.
2. `houve_sinais_duros` ficou binário `sim`/`nao`, como no pedido.
3. "Pandemia declarada" é a declaração da OMS: só 2009 e 2020. Gripes de 1957 e 1968 não contam.

**Recodificação às cegas:** um agente separado, sem acesso ao CSV, recodificou 10 episódios (UK-1980, SE-2018, US-1961, DE-1935, JP-1937, IL-2003, CN-1969, LT-2015, UA-2021, CH-1969) só com a regra.

| Coluna | Concordância na 1ª versão |
|---|---|
| Guerra no território (3 janelas × 10) | 28 de 30 células; 9 de 10 episódios |
| Participou de guerra em 60 meses | 7 de 10 |
| Sinais duros (com `parcial` lido como `nao`) | 8 de 10 (JP-1937 e UA-2021; UA-2021 corrigido para `sim`, porque reservistas e estado de emergência vieram em fev/2022, dentro do período) |

A divergência em guerra era minha: bombardeio de Taipé em fev/1938, em território sob controle japonês. **Corrigi JP-1937 para `sim` em 12 e 24 meses.** Também corrigi participação: UK-1980 para `nao` (a luta foi em território próprio), CN-1969 para `sim` (Paracels, jan/1974) e UA-2021 para `sim` (Kursk). Ficou a divergência em sinais de JP-1937: o outro codificador marcou `sim` com dúvida, eu mantive `nao`, porque a mobilização veio depois de iniciada a guerra na China. Os casos que ele marcou com dúvida são CN-1969 (fronteira contestada; se Tielieketi não contar, as 3 janelas viram `nao`) e IL-2003 (se o Líbano de 2006 contar como interestatal, viram `sim` em 60 meses).

**Limites a dizer sempre:**

- A seleção não é aleatória: é o que a busca achou em inglês, e a contagem de "pedidos em paz" é inflada pelo Ocidente da Guerra Fria e por 2024 e 2025.
- `houve_sinais_duros` foi codificado por mim conhecendo o resultado; a separação que ele mostra precisa ser lida com isso em mente.
- Datas de participação e desastre marcadas "sem captura" na observação são conhecimento geral, sem texto capturado. Valor `nao` em desastre é ausência de achado.
- `guerras_sem_campanha.csv` é lista de exemplos, sem denominador e com "não encontrada" no lugar de "não houve". Não permite calcular quantas guerras tiveram campanha.
