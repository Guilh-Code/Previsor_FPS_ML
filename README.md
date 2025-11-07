# 🖥️ Simulador de Performance (FPS) em Jogos - Um Projeto de Machine Learning

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://previsorfps.streamlit.app/)

**Confira o aplicativo web interativo:** [**[Clique aqui para usar o Previsor de FPS]**](https://previsorfps.streamlit.app/)

---

## 🚀 Sobre o Projeto

Este projeto transforma a complexa tarefa de prever a performance de um computador em uma ferramenta web simples e interativa. O objetivo é estimar o **FPS (Frames Per Second)** que um usuário pode esperar ao combinar diferentes CPUs, GPUs e configurações gráficas em diversos jogos.

O que começou como um projeto de estudo pessoal para entender o mercado de hardware se transformou em um pipeline completo de Data Science, desde a coleta de dados brutos até o deploy de um modelo de Regressão.

### 💡 Motivação

A motivação inicial foi canalizar a ansiedade e a empolgação pela montagem de um novo PC (um presente de aniversário) em um projeto de portfólio produtivo. O objetivo era unir a paixão por hardware com a prática de ciência de dados, respondendo à pergunta: "Será que conseguimos prever a performance de um PC antes de comprá-lo?".

---

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído usando um stack de ferramentas de Data Science moderno:

* **Linguagem:** Python
* **Banco de Dados:** SQLite (para análise)
* **Análise e Manipulação:** Pandas
* **Machine Learning:** Scikit-learn (RandomForestRegressor, Pipeline, ColumnTransformer)
* **Serialização do Modelo:** Joblib
* **Aplicativo Web:** Streamlit
* **Hospedagem:** Streamlit Community Cloud

---

## 📈 A Jornada do Projeto (Metodologia)

O projeto foi dividido em 5 fases principais:

### Fase 1: Coleta e Engenharia de Dados
O primeiro passo foi criar um dataset realista do zero. Foram criadas 10 tabelas CSV (ex: `dim_CPU`, `dim_GPU`, `dim_Jogo`) para simular um banco de dados relacional de uma loja de hardware. A tabela principal, `fact_Performance`, foi populada com **482 linhas** de benchmarks sintéticos, mas de alta fidelidade, baseados em padrões de performance reais do mercado (Novembro de 2025).

### Fase 2: Análise Exploratória de Dados (SQL)
Com os dados em um banco SQLite, uma série de mais de 15 "Desafios SQL" foi realizada para extrair insights e entender o dataset. As consultas evoluíram de simples `SELECT`...`WHERE` para `JOIN`s quádruplos, agregação (`GROUP BY`), CTEs (`WITH`) e lógica de negócios complexa (como `JOIN ON a.valor <= b.limite`).

**Principais descobertas da análise SQL:**
* Cálculo do KPI **"Custo por FPS"** (`preco_medio_brl / AVG(fps_medio)`).
* Identificação de viés (bias) em médias "gerais" e a necessidade de **segmentar** a análise (eSports vs. Jogos AAA).
* Análise de compatibilidade física (ex: Air Coolers vs. Gabinetes) usando *non-equi joins*.

### Fase 3: Engenharia de Atributos (A `MasterTable`)
Para treinar o modelo, as 4 tabelas principais (`fact_Performance`, `dim_CPU`, `dim_GPU`, `dim_Jogo`) foram unificadas em uma única **"Tabela Master"** (`Tabela_ML_FPS`) usando SQL. Esta tabela denormalizada serviu como o dataset de treino final.

#### Amostra da `Tabela_ML_FPS`:

| fps_medio | nome_gpu | memoria_gb_gpu | consumo_tdp_watts_gpu | gpu_preco | nome_cpu | cpu_nucleos | cpu_clock | cpu_preco | nome_jogo | jogo_genero | jogo_exigencia | resolucao | qualidade_grafica |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 390 | RTX 5060 | 8 | 140 | 2200.0 | Ryzen 5 9600X | 6 | 5.4 | 1500.0 | Valorant | FPS Competitivo | Baixo | 1080p | Alto |
| 350 | RTX 5060 | 8 | 140 | 2200.0 | Ryzen 5 9600X | 6 | 5.4 | 1500.0 | Counter-Strike 2 | FPS Competitivo | Baixo | 1080p | Alto |
| 510 | RTX 5060 | 8 | 140 | 2200.0 | Ryzen 5 9600X | 6 | 5.4 | 1500.0 | League of Legends | MOBA | Muito Baixo | 1080p | Alto |

### Fase 4: Treinamento do Modelo (Machine Learning)
O objetivo era prever o `fps_medio` (alvo `y`).
1.  **Pré-processamento:** Foi construído um `Pipeline` complexo no `scikit-learn` para preparar os dados. Ele usa um `ColumnTransformer` para aplicar `StandardScaler` (em features numéricas), `OneHotEncoder` (em features categóricas) e `OrdinalEncoder` (em features ordinais como "Baixo", "Médio", "Alto").
2.  **Modelo:** Foi treinado um `RandomForestRegressor` (`n_estimators=100`) nos dados.
3.  **Resultado:** O modelo alcançou métricas excelentes, provando que os padrões no dataset eram fortes:
    * **R² Score (R-quadrado): `0.89`** (Nosso modelo consegue explicar 89% da variação do FPS).
    * **MAE (Erro Médio Absoluto): `~28 FPS`** (Em média, as previsões do modelo erram em 28 FPS, para mais ou para menos).

### Fase 5: Deploy (Aplicativo Web)
O `Pipeline` treinado (pré-processador + modelo) foi salvo em um arquivo `.joblib`. Um aplicativo web foi construído usando **Streamlit**, permitindo que qualquer usuário selecione peças de hardware e configurações de jogo em menus dropdown e receba uma previsão de FPS instantânea. O app foi hospedado no Streamlit Community Cloud.

---

## 🌟 Principais Descobertas
* A `RX 6600` e a `RX 7600` se mostraram as rainhas do **Custo-Benefício** (Menor R$/FPS) em ambas as análises (eSports e AAA).
* Placas "Enthusiast" (como `RTX 4090`) possuem o pior custo-benefício, chegando a custar **+120 R$/FPS** em jogos AAA.
* A `qualidade_grafica` é uma *feature* (característica) com peso quase zero em jogos de eSports (como League of Legends), mas é a *feature* mais impactante em jogos AAA (como Cyberpunk 2077) — e o modelo de ML aprendeu isso sozinho.

## 🔮 Próximos Passos
* **Modelo 2 (Previsão de Orçamento):** Criar um segundo modelo que, com base em um "FPS desejado" ou uma "placa de vídeo principal", use Machine Learning para sugerir as outras peças e prever o **orçamento total** do PC.

---
