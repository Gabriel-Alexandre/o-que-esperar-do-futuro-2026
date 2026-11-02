# Revisão adversarial

Feita em 02/nov/2026, por um agente que não codificou a base. Nenhum outro arquivo do projeto foi alterado e nada foi commitado. Os números abaixo foram recalculados a partir de `dados/derivados/`. O que vem de conhecimento geral, sem captura, está marcado. Decidir o que muda é do autor do projeto.

**Veredito curto.** Os dados conferem com as fontes na ampla maioria das linhas. O que não se sustenta é o caminho entre a base e as conclusões: o "8%" muda de 0 a 31% conforme regras defensáveis, 3 dos 9 casos de guerra falham a própria regra de entrada, os cenários não têm conta por trás nem regra de resolução, e dois pares de números se contradizem.

Em cada objeção, **Tamanho** diz se muda número principal (`g04`, `g07` ou uma previsão) ou só texto e dado de apoio.

---

## 0. O número que mais depende de escolha

Campanha sem sinais duros, guerra no território em 60 meses:

| Regra | k de n | % | Wilson 95% |
|---|---|---|---|
| Sem iniciadores, sem conflito já em curso, sem Malvinas | 0 de 23 | 0,0 | 0,0 a 14,3 |
| Só depois de 1945 | 1 de 23 | 4,3 | 0,8 a 21,0 |
| Tábua de vida, com os 12 abertos contando até onde foram observados | 1 + 1 + 0 | 5,8 | não calculado |
| Somando 8 episódios de `paises.csv` que ficaram fora | 2 de 33 | 6,1 | 1,7 a 19,6 |
| **Publicado em `g04` e `PREVISOES.md`** | **2 de 25** | **8,0** | **2,2 a 25,0** |
| Um voto por país (`primeiro_de_cada_pais` aplicado a este grupo) | 2 de 13 | 15,4 | 4,3 a 42,2 |
| Sinal visto na data do pedido (UA-2021, IN-2025, CN-1969 passam para "sem") | 5 de 28 | 17,9 | 7,9 a 35,6 |
| As duas anteriores juntas | 5 de 16 | 31,2 | 14,2 a 55,6 |

A leitura honesta é "de quase zero a cerca de um terço, conforme a regra". Publicar 8% sozinho dá uma precisão que a base não tem.

---

## 1. Quem acha o projeto calmo demais

**1.1 O "sem sinais" olha para a frente, e hoje ninguém pode olhar.**
A regra conta sinal "no mesmo período de cerca de 12 meses". UA-2021 virou `sim` por causa de reservistas e estado de emergência de 22 e 23/fev/2022, dias antes da invasão. O próprio `sinais.csv` marca os mesmos fatos como `nao` em jan/2022. Em dez/2021, a Ucrânia estaria no grupo "só o pedido". O mesmo vale para IN-2025 (ordem no dia dos ataques) e CN-1969 (o pedido é o próprio sinal).
**Tamanho:** muda número principal. O 8% vira 17,9% (5 de 28), e o 87,5% vira 80% (4 de 5).
**Conserto:** duas colunas, `sinais_na_data_do_pedido` e `sinais_em_12m`, e a previsão usa só a primeira, que é a única observável hoje.

**1.2 Falta de sinal hoje não limita um horizonte de 38 meses.**
`PREVISOES.md` diz "hoje nenhum país chegou lá, e por isso D fica baixo". Na base, das 7 guerras com sinal, 5 começaram em até 12 meses e 6 em até 24. O sinal duro tem alcance curto. Ele informa sobre 2027, muito pouco sobre 2029.
**Tamanho:** o 7% pode ficar (ver 2.3), mas perde esta justificativa.
**Conserto:** reescrever a âncora: "sem sinal duro hoje pesa até o fim de 2027; depois disso o número vem de outra base". Escrever também a regra de atualização: qual sinal, em qual país, move D para quanto.

**1.3 "Nenhum país chegou lá" contradiz o `sinais.csv`.**
HOJE-PL marca `mascara_iodo_abrigos_publicos = sim` (programa de PLN 102,4 bi), e PL-2025 tem `houve_sinais_duros = nao`. No placar de 10 itens, Suécia (2,5 de 5, 50%), Polônia (2,5 de 6, 42%), Finlândia (1,5 de 4, 38%) e Alemanha (2,5 de 7, 36%) ficam acima da Ucrânia em jan/2022 (2,5 de 8, 31%), e Taiwan e Japão (33%) também. Há ainda 120 mil pessoas no plano de evacuação de Sakishima e racionamento em plano na Alemanha e em Taiwan, com a régua de "evacuação planejada" aplicada a 1939.
**Tamanho:** muda o texto da âncora e, se a coluna for refeita, o rótulo de PL-2025. O número segue igual porque PL-2025 está aberto.
**Conserto:** trocar por "só a Polônia marca um sinal duro, e é um programa de abrigos de 2027 a 2031", e aplicar a mesma régua de "plano" a todos os momentos.

**1.4 O cenário A é onde tudo cai.**
Só C trata de combate declarado, e só com a Rússia. D exige grandes potências em combate direto. Invasão de Taiwan sem os EUA, bloqueio com tiro, Coreia, Índia e Paquistão, uso de arma nuclear em guerra regional: nada disso tem lugar além de A, descrito como "guerras longe, efeito limitado". P05 a 4% até 2027, com risco constante, dá 10,5% até 2029; o mercado (9,5%) daria 23,7%. A guerra EUA e Irã, em curso desde fev/2026, também fica em A. Assim o "45% de atrito" contém eventos que ninguém chamaria de atrito.
**Tamanho:** muda número principal.
**Conserto:** cenário E, "guerra grande fora da OTAN ou arma nuclear usada", tirado de A, com chance própria.

**1.5 "Combate declarado" deixa de fora o que os serviços de inteligência alertam.**
A fonte do BIS tcheco (`ibtimes-espioes-meses`) fala em operação "deliberately ambiguous", feita para deixar o governo na dúvida. C e P12 exigem declaração. Drone com mortos e sem declaração é, ao mesmo tempo, "sinal que confirmaria" C e um evento que não é C.
**Tamanho:** muda como C e P12 serão medidas.
**Conserto:** resolver P12 por fato, "ataque atribuído à Rússia pelo governo do país, com ao menos 1 morto em território de membro", sem a palavra "declara".

**1.6 As âncoras escolhidas puxam para baixo.**
A tabela usa o mercado de US$ 12 mil e deixa fora o de maior volume sobre o assunto: "NATO x Russia military clash by December 31, 2026", 12,5%, US$ 3,5 milhões, regra de qualquer uso de força. Também ficam fora a avaliação francesa que antecipa o ataque de 2030 para o outono de 2027 e a janela de 7 a 8 meses de Tusk, as duas em textos já capturados. E "sem ameaça iminente" é a fala de um funcionário anônimo, via Reuters, via Euromaidan Press, de 30/ago. "Iminente" não justifica ficar abaixo do mercado num prazo de 14 meses, e a tabela a chama de "oficial".
**Tamanho:** não muda número sozinho, mas muda o que sustenta P04 e C.
**Conserto:** incluir essas três âncoras, dizer por que cada uma pesa pouco, e atribuir a frase da OTAN como ela é.

**1.7 Os títulos do Brasil escondem o choque que os próprios dados mostram.**
`g10`, "ainda não mostra o choque": o IPCA de alimentação no domicílio foi de -0,09% em fev para 4,21% em set, com 1,94, 1,64 e 1,65 de março a maio, junto com o diesel (6,04 para 7,28, agora 6,70). A causa não está isolada, mas "não mostra" não cabe. `g09`, "já voltou boa parte": o preço voltou inteiro (406,9 em fev, 406,2 em set), e o que caiu foi o volume, 21,5% de jan a set contra 2025 (16,8% de março a set). O gráfico não mostra volume, termina em setembro, e a pesquisa registra uma alta em outubro que ele não alcança. Preço médio de importação também vem de contrato fechado antes.
**Tamanho:** só título e gráfico.
**Conserto:** `g10`: "subiu de zero para 4,2% desde a guerra; a causa não está separada". `g09`: preço e tonelada no mesmo gráfico.

**1.8 Regra aplicada mais forte contra a guerra em um caso.**
PL-2025 tem "drones russos em set/2025 não contam: sem combate terrestre nem limiar". A regra diz "combate **ou** bombardeio por outro Estado", e não exige combate terrestre. Bombardeio isolado de Taipé contou para JP-1937, e P04 usa regra em que drone de ataque conta. Se valer, PL-2025 vira `sim` em 12 meses. O mesmo risco existe em UK-2024 (drone em Akrotiri, autor não dito na fonte lida).
**Tamanho:** 24 meses vai de 8 de 40 para 9 de 40 se Akrotiri for atribuído ao Irã. 60 meses não muda.
**Conserto:** dizer o critério certo no campo `observacao` (drones sem alvo em território polonês, por exemplo) ou mudar o código; emenda datada.

---

## 2. Quem acha o projeto alarmista

**2.1 Os 25% e 23% não têm conta.**
Nenhuma linha de "De onde vêm os números" chega a 25 ou 23. A âncora de base diz "o mundo tem muitos países, então o cenário fica acima", sem dizer quantos países nem quanto acima. Com 8%, 10 países da linha de frente e independência, sairiam 41%; com o mercado, por outro caminho, cerca de 44% para ataque russo em país da UE até 2029 (hazard de 15,9% ao ano em 2027 mantido); com a mesma conta, 36% partindo de P04. Nenhuma dessas contas está no projeto. "23%" e "25%" dentro de faixas de 15 a 30 e 15 a 35 são precisão falsa, e o 23 existe para a soma dar 100.
**Tamanho:** muda como o número principal é apresentado.
**Conserto:** escrever a cadeia de C ("ataque em país da UE até 2029 × chance de ter mortos e atribuição"), e mostrar "cerca de 1 em 4" com a faixa. Em `g07` as barras mostram a faixa, além do ponto.

**2.2 C e B ficam muito acima da história, e o texto não diz.**
C a 25% em 38 meses equivale a 9,1% ao ano. Combate com mortos entre Rússia e membro da OTAN aconteceu uma vez em cerca de 77 anos (Su-24 e Turquia, 2015; conhecimento geral, sem captura), 1,3% ao ano. É um fator de 7. Para B, com zero caso em cerca de 16 anos desde Stuxnet (conhecimento geral), a regra de Jeffreys dá 9% e a de Laplace 18% em 38 meses, e o maior ataque real em país rico na base foi um "small energy generator" que "did not pose any threat" à rede (`lbc-usina-quatro-dias`).
**Tamanho:** muda número principal para B (ver 3.3). C pode ficar, se o multiplicador for defendido por escrito.
**Conserto:** colocar a taxa histórica e o multiplicador na tabela de âncoras, e dizer o que justifica cada um.

**2.3 D não é alarmista, mas ninguém escreveu isso.**
7% em 38 meses é 2,3% ao ano. Uma única guerra direta entre grandes potências desde 1945 (Coreia; conhecimento geral) daria 3,9% em 38 meses. O número fica menos de 2 vezes acima dessa base.
**Tamanho:** nenhum.
**Conserto:** registrar a conta.

**2.4 A base puxa para guerra, ainda que sem intenção.**
A regra promete casos de desastre e bug porque "são os casos sem guerra que a lista precisa ter". O resultado: `ameaca_estatal` é `sim` em 31 de 46 linhas e `nao` em só 3 (US-1999, JP-1999, NO-2018). Pelo menos 8 candidatos com data fechada em `paises.csv` ficaram fora: Irlanda 2019, Estônia 2018, Letônia 2020, Canadá 2007, México 2018, Argentina 2018, Itália 2012, Bélgica 2018. Campanhas de terremoto do Japão, Nova Zelândia e Chile não aparecem. Com só esses 8: todos 9 de 41 (22%, contra 27,3%), sem sinais 2 de 33 (6,1%).
**Tamanho:** muda 60m "todos" e, pouco, o 8%.
**Conserto:** cruzar `paises.csv` com a lista, incluir ou registrar o motivo de cada exclusão no §5 da regra.

**2.5 Régua dupla na entrada, a favor do caso com guerra.**
Coreia do Sul 2017 e 2023 saíram por "exercício de sirene, sem ação em casa". IN-2025 é sirene, blecaute simulado e evacuação em exercício, e a própria linha diz "pedido fraco na condição 3" e "ataques do mesmo dia". EUA 2017 saiu por ser governo estadual; UA-2021 entrou com emissor vice-prefeito de Kyiv, e a linha admite isso, embora a condição 1 exclua prefeitura. CN-1969 é "pedido coletivo, não de casa em casa", depois de o conflito começar em março.
**Tamanho:** muda número principal. Sem as três linhas: com sinais 4 de 5 (80%, de 37,6 a 96,4), todos 6 de 30 (20%, de 9,5 a 37,3), 24 meses 5 de 37 (13,5%), depois de 2000 **0 de 9** contra os 18,2% publicados.
**Conserto:** tirar as três da taxa, ou reabrir Coreia e os outros pela mesma régua. Se saírem, UA-2021 fica como estudo de caso em separado, porque é o contraexemplo mais importante do projeto.

**2.6 O numerador mistura coisas que não respondem à pergunta.**
Dos 9 casos: DE-1935 e JP-1937 são de quem iniciou a guerra, CN-1969, UA-2021 e IN-2025 são de conflito já aberto, e UK-1980 é um arquipélago no Atlântico Sul sem relação com a ameaça soviética. Sobram UK-1938, UK-1939 e IL-1990. "O país pediu estoque e depois foi atacado por quem temia" é 3 de 27 (11,1%), todos antes de 1991.
**Tamanho:** muda a leitura de 27,3% e 36% se forem citados. `primeiro_de_cada_pais` a 41,2% não pode sair sozinho.
**Conserto:** coluna `guerra_com_o_ameacante_declarado` e mostrar esse recorte.

**2.7 A censura favorece o sim.**
A emenda 1 conta `sim` com janela aberta (UA-2021, IN-2025) e tira do denominador os 12 abertos sem evento. Todos os 12 estão em "sem sinais". Na tábua de vida: todos 21,4% (publicado 27,3%), depois de 2000 9,1% (publicado 18,2%), sem sinais 5,8%.
**Tamanho:** muda 60m "todos" e "depois de 2000".
**Conserto:** publicar a tábua de vida ao lado, ou trocar por ela.

**2.8 Títulos.**
`g03` "O termômetro de guerra existe": rho -0,30, p = 0,139, e sem Singapura o resultado passa a p = 0,043, então depende de um ponto só. `g05` "O que governos fazem quando esperam guerra": a barra de "hoje" vem de uma proporção entre itens com dado, e põe a Suécia (5 de 10 sem dado) acima da Ucrânia pré-invasão, enquanto os EUA aparecem com 0% com 8 de 10 sem dado, no assunto central do projeto. `g07` não exagera no título, mas soma visualmente 55% de "algo pior que atrito", sem dizer o que nunca aconteceu antes.
**Tamanho:** só título e gráfico.
**Conserto:** `g03`: "Há um sinal fraco, que não dá para separar do acaso". `g05`: mostrar placar sobre 10, com os itens sem dado em cinza, e não comparar quem tem menos de 7 itens; buscar os itens dos EUA antes de plotar.

---

## 3. Auditor de método

**3.1 ACH: H2 não pode ser derrubada, e H1 é um espantalho.**
H2 tem 20 C, 1 N, 0 I em 21 evidências. Uma hipótese que é compatível com tudo não ganhou nada, e o próprio texto da pesquisa diz, no §5: "pedir 3 dias é compatível com quase todas as hipóteses, e por isso diz pouco". A hipótese que falta é a que o leitor tem na cabeça: **"governos acham guerra plausível em poucos anos, sem data"**. Hoje ela está dentro de H2 (E09, "testes em meses", está marcada como C para H2). H1, "guerra datada", ninguém sério defende, conforme a própria pesquisa ("ninguém declarou saber de guerra marcada").
Além disso, E01 (prazo curto, peso alto, I contra H1) é desmentida pelos dados do projeto: UK-1939 pedia "cerca de uma semana" 7 meses antes da guerra e UA-2021 pedia comida para 2 dias, 2 meses antes da invasão. E03, E05, E20 e E21 também não contradizem guerra sem data. Refeita com a hipótese nova, nenhuma das 21 linhas a separa de H2 com clareza.
Só uma IA classificou. A base de episódios teve recodificação às cegas; o ACH não.
**Tamanho:** muda `g06` e o achado "por que agora". `resultados/hipoteses.csv` deixa de dar um vencedor.
**Conserto:** H1a (data sabida) e H1b (plausível sem data), H2 estreita ("seguro geral, sem cenário de guerra em mente"), hipóteses excludentes, E01 recodificada, recodificação às cegas de ao menos as evidências de peso alto, e a frase final: "o método elimina a guerra datada; ele não elimina guerra plausível".

**3.2 P12 contra C + D.**
P12 acontecendo põe o mundo em C ou D. Logo P12 = (C com combate em território de membro) + (D com combate em território de membro). Se 85% a 100% de C é em território e cerca de 60% de D também, P12 fica entre 25 e 29. O 25% só fecha no canto mais baixo. **Tamanho:** muda previsão. **Conserto:** P12 a 28%, ou definir C como "P12 e não D" e baixá-lo para cerca de 21%.

**3.3 P06 contra B.**
P06, 10% em 14 meses, com risco constante, dá 24,9% em 38 meses. B é o evento sem C nem D. Com independência, B = 24,9 × 0,68 = 16,9%. Para B ser 23%, o evento total teria de ser 33,8%, e P06 deveria ser 14,1%. Se o evento for mais provável em guerra, o que é o caso, a distância cresce. **Tamanho:** muda número principal. **Conserto:** escolher um par, P06 10% e B 17%, ou P06 14% e B 23%. Pela leitura 2.2, o primeiro é mais fácil de defender.

**3.4 P11 contra B.**
P11 (40% até 2027) é quase o "sinal que confirmaria" B. Um sinal que dispara em 40% dos mundos em 14 meses, para um cenário de 23% em 38 meses, confirma pouco. A usina britânica de jul/2026 e os 100+ sistemas de água já são casos parecidos: P11 precisa dizer se evento anterior a 02/nov com atribuição posterior conta. Os outros sinais têm o mesmo problema: "artigo 4 repetido" e "drone" já aconteceram. **Tamanho:** só resolução. **Conserto:** data de corte em P11, e um limiar por sinal que ainda não tenha sido cruzado.

**3.5 Os cenários não podem ser medidos.**
"Pior ponto" exige ordem, e ela não está escrita: `PREVISOES.md` lista A, B, C, D e `g07` lista A, C, B, D. Com B e C no mesmo mundo, qual vale? A não tem critério de resolução. B diz "país rico", P06 diz OCDE; B diz "sem serviço", P06 diz "luz ou água". O texto promete nota de Brier, e `conferir_cenarios.py` só testa `45 + 23 + 25 + 7 == 100`, uma conta literal que não lê nenhum arquivo.
**Tamanho:** sem isto, o número principal não é cobrável.
**Conserto:** `resultados/cenarios.csv` (previsto no `PLANO.md` e ausente) com ordem, critério de cada cenário e prioridade em caso de empate, e o script lendo o arquivo.

**3.6 Proposta de números coerentes, como emenda datada.**

| Cenário | Original | Proposta | Por quê |
|---|---|---|---|
| A | 45 | 44 | ganha 6 de B e 4 de C, perde 11 para E |
| E (novo) | | 11 | 1.4: Taiwan até 2029 sozinho dá 10,5 pela P05 |
| B | 23 | 17 | 3.3, com P06 mantida |
| C | 25 | 21 | 3.2, com P12 mantida |
| D | 7 | 7 | 2.3 |

É uma opção, e ela soma 100. O original fica no git, e as duas versões são medidas.

**3.7 "Antes de qualquer medição" não é verdade.**
O commit `3ddc6cd` (10:29:15) já traz "2 de 25", "7 de 8" e "2,5 de 8". `historia_episodios.csv`, `sinais.csv` e `hipoteses_evidencias.csv` têm data de 10:26 e 10:27, e os mercados de 09:53. As previsões do Brasil (`35a3538`, 10:35:35) vêm depois dos derivados do Brasil (10:34 e 10:35). `PLANO.md` e o texto de `PREVISOES.md` prometem o contrário. O que elas antecedem é o futuro, e foram escritas sem gráficos. O arquivo também tem P08 e P16 com palavra alterada e não commitada, e "as previsões acima" aponta para uma tabela que não está acima.
**Tamanho:** não muda número; é a credibilidade do registro.
**Conserto:** "escritas depois de medir o passado, antes do futuro e antes dos gráficos"; commit da troca de palavras com a explicação.

**3.8 Escala.**
`metodo/wikipedia-wep.txt` **não tem a ICD 203**: zero ocorrências de "ICD" e nenhuma faixa numérica dela. Ela traz Kent, PHIA, Mercyhurst e o NIC sem números. A pesquisa registra que o PDF do DNI recusou. As faixas de `PREVISOES.md` batem com a ICD 203 de memória (conhecimento geral), mas a fonte citada não as sustenta. Na mesma captura, Kent põe "almost certainly not" em 7%, mais ou menos 5.
Três erros de uso: o 5% tem duas palavras (P03 "muito improvável", P14 e P17 "quase impossível"). O termo oficial é "almost no chance" ou "remote", e **"quase impossível" soa bem mais forte**: P05 a 4%, contra 9,5% do mercado, diz que a invasão de Taiwan é "quase impossível" para 1 chance em 25. A coluna se chama `palavra_ic203`. Faixas de D (3 a 12), B e C atravessam duas palavras, o que deve ser dito.
**Tamanho:** só palavra. **Conserto:** capturar a ICD 203 (ou cópia) e citá-la, regra de borda ("até 5% exclusive"), "quase nenhuma chance", renomear a coluna.

**3.9 Fonte não lida sustentando número.**
"Inteligência dos EUA, mar/2026: China sem plano para 2027" justifica ficar a menos da metade do mercado em P05. A própria pesquisa diz "só por resultado de busca e Military Times; capturar o relatório". A única captura com "Annual Threat Assessment" é uma matéria de 2025, sobre outro relatório, que diz o contrário em tom ("stronger coercive pressure"). Isso fere a regra "número só depois de lido".
**Tamanho:** P05 perde a âncora; a mudança seria grande se ela não for achada.
**Conserto:** capturar o relatório. Se não der, P05 fica perto do mercado ou a justificativa muda.

**3.10 "13 casos sem nenhum sinal público".**
`guerras_sem_campanha.csv` só diz "campanha não encontrada", com 9 de 13 em confiança baixa e sem busca específica. Geórgia 2008 "iniciou a ofensiva", Armênia 2020 tinha conflito aberto, Hungria e Tchecoslováquia foram atacadas pelos aliados. **Tamanho:** só texto. **Conserto:** "sem campanha à população encontrada".

**3.11 Sem grupo de comparação.**
`g04` diz "O pedido não avisa nada". Isso exige saber a taxa de guerra em países **sem** campanha, e o projeto não tem esse número (o próprio §5 diz que não dá). 8% em 5 anos pode ser mais que a taxa normal de um país. **Tamanho:** o título cai. **Conserto:** título descritivo agora; calcular a taxa-base por país e janela com UCDP como rodada seguinte.

**3.12 Wilson e validação.**
`wilson()` está certa (conferi 2 de 25, 7 de 8, 9 de 33), e o Brier (0,16, 0,084) e o Spearman reproduzem. Mas o intervalo pressupõe amostra aleatória e independente, e aqui há 5 episódios do Reino Unido, 5 da Suécia e 5 dos EUA, escolhidos por busca. "A margem de 95%" em `g04` promete mais do que dá. `VALIDACAO.md` reconta o mesmo CSV: confirma a soma, sem testar a codificação. E `primeiro_de_cada_pais` trata Alemanha e Alemanha Ocidental como países diferentes.
**Tamanho:** só leitura. **Conserto:** legenda "faixa mínima; a amostra não é aleatória", e `Alemanha Ocidental` como `Alemanha` nesse recorte.

---

## 4. Conferência na unha

**Sorteio.** Python `random.Random(seed).sample` sobre a ordem dos CSV: episódios com seed `20261102`, países `20261103`, interrupções `20261104`, ureia `20261105`.

### Episódios (12 de 46)

Além da amostra, varri as 46 linhas: `trecho_curto` está em pelo menos uma das capturas em todas.

| Id | Trecho e data | Observação |
|---|---|---|
| UK-1980 | ok | maio de 1980 e 2/abr/1982 conferem |
| UK-2024 | ok | a 2ª fonte é o site de 2026, não prova 2024 |
| SE-1961 | ok | mês é marcador. Conversation diz "the last time" em 1961; a Wikipédia, na mesma linha, diz 1943 a 1991 |
| US-1950 | ok | mês aproximado, como dito |
| US-1961 | ok | |
| JP-1999 | ok | uma fonte, como dito |
| JP-2017 | ok | condição 3 fraca, como dito |
| IL-1990 | ok | a CIA confirma sala vedada, água e comida |
| FI-2024 | ok | conflito com `paises.csv`, ver abaixo |
| LV-2024 | ok | marcada `baixa`, mas o PDF oficial de 2024 está capturado em `lva-buklets` |
| TW-2025 | ok | 9,8 milhões confere |
| **UA-2021** | ok | **emissor é vice-prefeito de Kyiv: falha a condição 1**. Os boletins citados são de jan/2022 |

**12 de 12 no trecho, 1 de 12 falha a própria regra de entrada.** Fora da amostra, IN-2025 e CN-1969 têm o mesmo problema.

### Países (8 de 38)

| País | Resultado | Observação |
|---|---|---|
| Alemanha | ok | |
| Dinamarca | ok | nota oficial de 15/06/2024; `historia_episodios` usa 2024-07 por fonte única |
| Finlândia | trecho ok | é a página da ONG; o guia do Ministério (FI-2024, com "military conflict") não entrou, e data e `menciona_guerra = nao` ficam errados |
| Estônia | ok | |
| Letônia | ok | |
| **Polônia** | **data errada** | a própria captura diz "Warszawa, 2022 r. Wydanie I"; a linha diz 2025. Falta também o episódio PL-2022 |
| Croácia | ok | os 2 dias são da mala de evacuação, não do estoque de casa |
| Espanha | ok | regional |

Fora da amostra: Canadá aponta para `can-72h-pub`, e o trecho está em `can-2007`. A nota "38 de 38, 0 divergência" não fecha, porque Brasil e Portugal não têm trecho. Lituânia tem `menciona_guerra` vazio, com o guia "What to do in case of crisis or war" capturado em `ep-lituania-2024-iidraudimas`. Com Finlândia e Lituânia, **"10 de 33" vira 12 de 33**, e E04 e `g01` e `g03` mudam. Reino Unido fica como caso à parte: o discurso de 2024 cita guerra (`gbr-lbc`), a página atual não.

### Interrupções (6 de 10)

| Caso | Resultado | Observação |
|---|---|---|
| Greve 2018 | ok | 11 dias em Poder360 e Suno; Wikipédia 21 a 30/mai, como dito |
| Apagão 2023 | ok | 6 h no Sindiconet, 23.368 MW no TCU, 25 estados e DF |
| RS 2024 | ok | "afetados" é o número geral da enchente, sem medir serviço |
| **Enel out/2024** | **erro em um número** | 6 dias e 3,1 milhões conferem. O slide de comparação da Enel, p. 10, põe "Máximo de clientes simultâneos: 2,1 milhões" na coluna esquerda, **03/nov/2023** (posição conferida no PDF). A fonte citada não sustenta os 2,1 milhões em 2024 |
| Seca AM 2023 | ok | |
| Seca AM 2026 | ok | |

A coluna `pessoas` mistura clientes, pessoas e famílias, e P16 e P07 falam em pessoas. `g11` põe a greve como "dias sem serviço", e a nota diz que não é falta total.

### Ureia (3 anos sorteados contra `comex-ureia-pais.json`)

| Ano | Toneladas | Dentro do Golfo % | Omã % | Preço |
|---|---|---|---|---|
| 2017 | 5.423.823,4 ok | 52,36 igual ao CSV, **mas com erro** | 6,70 ok | 229,3 ok |
| 2025 | 7.725.046,7 ok | 19,84 ok | 15,56 ok | 395,4 ok |
| 2026 | 3.532.750,0 ok | 12,37 ok | 11,96 ok | 445,5 ok |

**Erro achado:** `DENTRO_DO_GOLFO` em `derivar_brasil.py` tem "Kuweit", e o ComexStat escreve "Coveite (Kuweit)". O Kuwait fica fora do Golfo: 2015 +6,41 pontos, 2016 +3,87, 2017 +3,64 (52,36 vira 56,00), 2018 +6,75, 2019 +0,22, 2021 +0,51, 2022 +0,04. De 2023 em diante, nada. `g08` começa em 2019 e quase não muda.

A comparação de `g08` com os 41% junta país de origem com "passou por Ormuz". A fonte do número viral diz 17% vindo do Irã, e o ComexStat dá 2,39%, o que reforça o título. Mas o preço da ureia de Nigéria e Rússia também responde a Ormuz, e isso o gráfico de origem não mede.

---

## 5. Decisão

### Conserto obrigatório antes de publicar

| # | O quê | Onde | Muda número principal? |
|---|---|---|---|
| 1 | Tirar UA-2021, IN-2025 e CN-1969 da taxa, ou reabrir Coreia e outros pela mesma régua (2.5) | `historia_episodios.csv`, `analise.py` | sim: 7 de 8 vira 4 de 5; depois de 2000, 0 de 9 |
| 2 | Separar sinal na data do pedido e mostrar a faixa do 8% (1.1, seção 0) | CSV, `g04`, `PREVISOES.md` | sim |
| 3 | `g04`: tirar "não avisa nada"; corrigir "de 1935 a 2021", que inclui 2025 (3.11) | `graficos.py` | não |
| 4 | Fechar P06 e B, e P12 e C + D (3.2, 3.3, 3.6), como emenda datada | `previsoes.csv`, `PREVISOES.md`, `g07` | sim |
| 5 | Criar cenário E e tirar a catch-all de A (1.4) | `PREVISOES.md`, `g07` | sim |
| 6 | Escrever ordem e regra de resolução dos cenários; criar `cenarios.csv`; script que lê o arquivo (3.5) | `resultados/`, `ferramentas/` | não, mas sem isso não há cobrança |
| 7 | Resolver P12 por fato, sem "declara" (1.5) | `previsoes.csv` | muda a medição |
| 8 | Refazer ACH com H1b, E01 recodificada e segundo codificador às cegas (3.1) | `hipoteses_evidencias.csv`, `g06` | muda o achado "por que agora" |
| 9 | Corrigir a âncora "nenhum país chegou lá" e "por isso D fica baixo" (1.2, 1.3) | `PREVISOES.md` | não |
| 10 | Incluir âncoras omitidas e capturar ou tirar a da China (1.6, 3.9) | `PREVISOES.md` | P05 pode mudar |
| 11 | Corrigir "antes de qualquer medição", "previsões acima" e commitar P08 e P16 (3.7) | `PLANO.md`, `PREVISOES.md` | não |
| 12 | Escala: capturar ICD 203, regra de borda, trocar "quase impossível", renomear coluna (3.8) | `previsoes.csv`, `PREVISOES.md` | não |
| 13 | Dados: Kuwait, Polônia 2022, Finlândia e Lituânia (12 de 33), Enel 2,1 milhões, Dinamarca 2024-06, captura do Canadá | `derivar_brasil.py`, `paises.csv`, `brasil_interrupcoes_longas.csv` | não |
| 14 | "13 casos sem nenhum sinal" vira "sem campanha encontrada" (3.10) | `PREVISOES.md` | não |
| 15 | Títulos e gráficos: `g03`, `g05`, `g09`, `g10`, `g11`; faixa em `g07` (1.7, 2.1, 2.8) | `graficos.py` | não |

### Registrar como limite

| Limite | Por que não se conserta agora |
|---|---|
| Amostra por busca, em inglês, inflada por Guerra Fria e 2024 e 2025; faltam França, Polônia, Holanda e Finlândia de 1939, Israel 1967, Golfo 1990 | exigiria nova coleta; o viés vai para os dois lados e o tamanho é desconhecido |
| `houve_sinais_duros` e o placar foram codificados conhecendo o resultado | uma recodificação às cegas só com texto anterior ao resultado reduziria, sem eliminar |
| Sem taxa de guerra em países sem campanha (3.11) | rodada seguinte, com UCDP |
| Tábua de vida e recortes por país, se não virarem o número principal (2.6, 2.7) | deixar publicados ao lado |
| Episódios faltantes de `paises.csv` (2.4), se não entrarem | registrar motivo por candidato |
| Cenários e previsões são julgamento de uma IA; as faixas são opinião, e o multiplicador sobre a história é argumento | natureza do exercício; dizer sempre |
| Mercados longos são finos (US$ 12 mil) e os curtos têm regra mais ampla que C | não servem de âncora direta |
| `sem_dado` de 2 a 8 em 10 nos momentos de hoje | buscar o que der (1.3, 2.8) e dizer o resto |
| `menciona_guerra` mede a palavra na página lida, e o motivo de governo fica fora | diferente de "o governo não pensa em guerra" |
| O termômetro depende de Singapura | fica como achado fraco |
| Os cenários ainda não dizem o que muda no Brasil em cada um; `docs/RODADAS.md` não existe | etapa seguinte do plano |
