# %%
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# %%

df = pd.read_csv('tabela_ML_fps.csv')
df.info()

# %%

# --- PASSO 2: DEFINIR FEATURES (X) E ALVO (y) ---

print("\n--- PASSO 2: Definindo Features e Alvo ---")

# O 'y' é o que queremos prever.
y = df['fps_medio']

# O 'X' é tudo o que usamos para a previsão.
# Vamos dropar (remover) o alvo E as colunas de "nome".
# O modelo vai aprender com as *características* (núcleos, preço, gênero)
# e não com o *nome* da peça, para evitar o Overfitting que falamos.
X = df.drop(columns=['fps_medio', 'nome_gpu', 'nome_cpu', 'nome_jogo'])

print("Alvo (y) definido (fps_medio).")
print("Features (X) definidas. Colunas usadas para previsão:")
print(X.info())

# %%

# --- PASSO 3: CRIANDO O PIPELINE DE PRÉ-PROCESSAMENTO ---
# O "cérebro" que vai transformar nossos dados.

print("\n--- PASSO 3: Criando o Pré-processador ---")

# 1. Definir quais colunas são de qual tipo (baseado no X.info())
numeric_features = [
    'memoria_gb_gpu', 'consumo_tdp_watts_gpu', 'gpu_preco',
    'cpu_nucleos', 'cpu_clock', 'cpu_preco'
]

categorical_features = [
    'jogo_genero', 'resolucao'
]

ordinal_features = [
    'jogo_exigencia', 'qualidade_grafica'
]


# 2. Definir as ordens para as colunas Ordinais

exigencia_cats = ['Muito Baixo', 'Baixo', 'Médio', 'Alto', 'Muito Alto', 'Extremo']
qualidade_cats = [
    'Baixo (Competitivo)', 'Baixo', 'Medio', 'Médio (DLSS Qualidade)', 'Médio (FSR Qualidade)',
    'Alto', 'Alto (DLSS Qualidade)', 'Alto (FSR Qualidade)', 'Muito Alto', 
    'Ultra', 'Ultra (DLSS Qualidade)', 'Ultra (FSR Qualidade)', 'Ultra (Max)',
    'Alto (DLSS Qualidade + RT)', 'Alto (FSR Qualidade + RT)'
]


# 3. Criar os "mini-pipelines" de transformação
numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())  # Padroniza a escala (ex: preço de 1500 vira 1.5)
])

categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

ordinal_transformer = Pipeline(steps=[
    ('ordinal', OrdinalEncoder(categories=[exigencia_cats, qualidade_cats], 
                                handle_unknown='use_encoded_value', 
                                unknown_value=-1)) # Transforma (Baixo=1, Medio=2...)
])

# 4. Criar o Pré-processador Mestre (ColumnTransformer)
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features),
        ('ord', ordinal_transformer, ordinal_features)
    ],
    remainder='passthrough'
)

print("Pré-processador criado com sucesso.")

# 5. Teste (Vamos ver quantas colunas ele cria)
# Vamos "treinar" o pré-processador e ver a forma final do nosso X
X_processado_teste = preprocessor.fit_transform(X)

print(f"\nDimensão original do X: {X.shape}")
print(f"Dimensão do X após Encoding: {X_processado_teste.shape}")

# Vamos ver quantas colunas o OneHotEncoder criou:
try:
    one_hot_features = preprocessor.named_transformers_['cat']['onehot'].get_feature_names_out(categorical_features)
    print(f"Features criadas pelo OneHotEncoder: {len(one_hot_features)} colunas")
    # print(one_hot_features) # Descomente esta linha se quiser ver o nome das colunas
except:
    pass # Versões mais antigas do sklearn não têm get_feature_names_out

# %%
# --- PASSO 4: DIVIDIR OS DADOS E TREINAR O MODELO ---

print("\n--- PASSO 4: Dividindo dados e treinando ---")

# 1. Dividir os dados (80% para treino, 20% para teste)
# random_state=42 garante que a divisão seja sempre a mesma, 
# para que possamos reproduzir nossos resultados
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Dados de Treino: {X_train.shape[0]} amostras")
print(f"Dados de Teste:  {X_test.shape[0]} amostras")

# %%

# Definir o Modelo

model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)

# 3. Criar o Pipeline de ML COMPLETO

ml_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', model)
])

# 4. Treinar o modelo
print("Treinando o modelo... (Isso pode levar alguns segundos)")

# O .fit vai rodar o preprocessor SÓ no X_train
# e depois treinar o modelo nos dados já processados.
ml_pipeline.fit(X_train, y_train)

print("Modelo treinado com sucesso!")
# %%

print("\n--- PASSO 5: Avaliando a performance do modelo ---")

# 1. Fazer previsões nos dados de teste
# O .predict vai rodar o preprocessor SÓ no X_test
# (usando as regras que ele aprendeu no X_train)
# e depois fazer a previsão com o modelo treinado.
y_pred = ml_pipeline.predict(X_test)

# 2. Avaliar a performance
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print("\n--- RESULTADOS DA AVALIAÇÃO ---")
print(f"R² Score (Coef. de Determinação): {r2:.4f}")
print(f"MAE (Erro Médio Absoluto): {mae:.2f} FPS")

# 3. Interpretando os resultados
print("\n--- Interpretação ---")
print(f"O R² (perto de 1.0 é bom) indica que nosso modelo consegue explicar {r2*100:.2f}% da variação do FPS.")
print(f"O MAE indica que, em média, as previsões do nosso modelo erram em {mae:.2f} FPS (para mais ou para menos).")

# %%


# --- PASSO 7: SALVANDO O MODELO PARA PRODUÇÃO ---
import joblib

MODEL_FILE_NAME = 'modelo_fps.joblib'

print(f"\n--- PASSO 7: Salvando o pipeline treinado em '{MODEL_FILE_NAME}' ---")

# Salva o objeto 'ml_pipeline' (que contém o preprocessor E o modelo)
joblib.dump(ml_pipeline, MODEL_FILE_NAME)

print("Modelo salvo com sucesso!")

# %%


