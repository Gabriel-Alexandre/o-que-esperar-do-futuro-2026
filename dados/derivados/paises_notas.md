# Notas de paises.csv (E1)

Captura em 02/nov/2026. Cada linha aponta para um texto lido em `oficiais/<nome>.txt`, que fica em
`documentacao/referencias-conteudo/roteiros/videos-longos/VIDEO_021_PREPARACAO_72_HORAS/referencias/textos/oficiais/`
(texto de terceiros, fora do git deste projeto; aqui entram o endereço e um trecho de até 20 palavras).

## Como foi montado

- 38 linhas: os 33 da lista da Newsweek, Bélgica, Portugal, Espanha, Itália e a União Europeia (linha de não país, `iso3` = EUU, que não é código ISO).
- Cada `trecho_curto` foi conferido por script contra o texto capturado (38 de 38 linhas, 0 divergência).
- `abrangencia` tem um valor extra, `supranacional`, só na linha da UE.
- Datas: AAAA-MM ou AAAA. Quando a data veio de metadado de página ou de PDF, a coluna `fonte_data_primeira` diz isso. Vazio = não achei.
- Cinco PDFs recusados pelo script por erro de certificado (Polônia, Suécia, Taiwan, Bélgica, guia de Taiwan em chinês) foram baixados com `curl -k` e o texto foi extraído com pypdf; o cabeçalho de cada `.txt` registra isso.

## Resultado em números

| Situação | Países da lista Newsweek (33) |
|---|---|
| Documento oficial lido com orientação | 30 (inclui 2 só regionais: África do Sul e Filipinas; Austrália só com texto solto do NEMA) |
| Sem documento oficial lido | 3: Lituânia (site recusou, só matéria), Índia (site fora do ar para mim), Brasil (página nacional lida não traz kit) |
| Prazo de 3 dias (72 h) em texto nacional lido | GBR, IRL, FRA, NLD, DNK, FIN, LVA, CZE, CAN, ISR, NZL, mais CHL (48 a 72 h) e JPN (3 a 7) e DEU (3 a 10) |
| Prazo maior que 72 h | NOR, SWE, EST, POL, CHE, TWN (7 dias), DEU (10), AUT (10 a 14), SGP (14 dias de comida) |
| Prazo menor que 72 h | ARG (1 dia), HRV (2 dias) |
| Orientação sem número de dias | USA, MEX, COL, AUS, e ITA fora da lista |
| Palavra guerra no documento | FRA, DEU, NLD, NOR, SWE, EST, LVA, POL, TWN, SGP (10 dos 33) e a UE |

## Data da primeira orientação achada (o que é novo e o que é antigo)

- Antigas (2022 ou antes): Suécia 1943 (folheto, relatório do MSB), EUA 2003, Canadá 2007, México 2018 (artigo mais antigo lido), Estônia 2018 (metadado), Argentina 2018 (metadado), Irlanda 2019, Letônia 2020, Filipinas 2021 (regional), Lituânia 2022 (matéria), Taiwan 2022.
- Novas (2024 a 2026): Reino Unido 05/2024 (matéria), Dinamarca 06/2024, França 11/2025, Holanda 11/2025, Tchéquia 11/2025, Polônia 2025, Irlanda campanha 08/2026, Bélgica guia 10/2026, UE 03/2025.
- Sem data de primeira orientação: Alemanha, Noruega, Finlândia, Áustria, Suíça, Croácia, Chile, Colômbia, Brasil, África do Sul, Japão, Israel, Índia, Singapura, Nova Zelândia, Austrália (16 dos 33).
- Cuidado: "data da primeira" é a mais antiga que li, não prova que não houve antes. Em Alemanha, Noruega e Japão há indício de edições anteriores (buscas) que não li.

## Surpresas e coisas que a lista da Newsweek não sustenta

1. Argentina: o kit do órgão nacional pede água e comida para UM dia (2018). Croácia pede 2 dias.
2. México: o artigo do CENAPRED não tem número de dias; o "72 h" mexicano veio de matérias, não de documento oficial lido.
3. Brasil: nenhuma orientação nacional de kit achada em gov.br/mdr. Só Defesas Civis estaduais (kit com 2 litros de água por pessoa por dia). Conferir no navegador antes de afirmar que não existe.
4. África do Sul e Filipinas na lista: o documento lido é da Cidade do Cabo e de um escritório regional do DSWD. Austrália: o NEMA fala em "several days" e dá "três dias" como exemplo; prazo real é por estado.
5. Estados Unidos e Índia: sem número de dias (Ready.gov diz "several days").
6. "72 horas" não é o padrão: nove países da lista pedem uma semana ou mais como meta (NOR, SWE, EST, POL, CHE, TWN, DEU, AUT e SGP, que pede duas semanas de comida).
7. Guerra: só 10 dos 33 documentos usam a palavra. Dinamarca explica na própria página de perguntas por que não escreve sobre guerra; a Bélgica não usa a palavra (matéria) e a Tchéquia diz que o guia é para crises não militares. Estados Unidos, Canadá, Japão, Nova Zelândia e Irlanda falam de clima e apagão.
8. Itália (fora da lista): o manual de 2012 não traz número de dias; Espanha só tem orientação regional (Catalunha); Portugal sem página de kit lida.

## Lacunas e limites

- Índia: o site do NDMA recusou a conexão; nenhuma página lida. Linha com confiança baixa e `abrangencia` sem_prazo vem da afirmação da Newsweek.
- Lituânia: lt72.lt deu 403. Só a matéria da LRT (20/05/2022). `menciona_guerra` fica vazio.
- Portugal: a página capturada do ANEPC não traz kit; a página de kit deu erro.
- Noruega: as páginas do Statsforvalteren sobre a mudança de 3 dias para 1 semana (05/2024) deram 404; essa mudança está só em resultado de busca.
- Finlândia: o site 72tuntia.fi é da associação de resgate (SPEK), que diz expor a recomendação das autoridades. Confiança media.
- Reino Unido: o folheto oficial de 2004 citado em buscas não foi achado; a data mais antiga é de matéria.
- Fiz buscas com restrição de domínio oficial para achar os endereços; o que vale é o texto lido, não o resumo da busca.

## Segunda passada (10 casos de maior dúvida, reabertos contra o .txt)

1. Estônia, data 2018: o PDF de 2020-03 tem "BE PREPARED TO COPE INDEPENDENTLY FOR A WEEK"; 2018 é metadado, deixei isso escrito.
2. Bélgica, data 2018: o folheto antigo tem a seção "Bereid je noodpakket voor" e nenhuma menção a 72 h ou 3 dias; mantive a data como metadado e sem prazo antigo.
3. Taiwan, prazo: "One week's supply minimum recommended" é o estoque da casa; mochila é de 1 a 3 dias. Manual de 2023 pedia "mais de 3 dias".
4. Suécia, uma semana: a string "Sju dagar - öva för att klara en kris en vecka" está em dinsakerhet.se; o folheto (swe-mcf) não traz o prazo.
5. Alemanha: corrigi a observação, porque "02.06.2026 Publikation" é da versão em Leichte Sprache, não do guia principal.
6. Singapura: o "two-week supply" está sob "Economic Defence"; ajustei a observação para não ligar o estoque à guerra sem o texto dizer.
7. Letônia: "for 3 days (or preferably for a week)" confirmado nas linhas 233 e 304 do PDF.
8. Polônia: "min. 7 dni" e "przetrwanie tygodnia" confirmados no PDF; a mochila fala em "kilka dni".
9. Suíça: título tinha travessão; troquei por hífen. Água (9 litros, cerca de 3 dias) e comida (1 semana) ficam separadas na observação.
10. Austrália: reclassificada como sem_prazo, porque o texto do NEMA dá três dias só como exemplo para pensar nos itens.
