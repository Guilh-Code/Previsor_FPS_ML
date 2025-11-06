import streamlit as st
import pandas as pd
import joblib

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Previsor de FPS",
    page_icon="🖥️",
    layout="wide"
)

# --- 2. CARREGAR O MODELO E OS DADOS ---

# Cacheia o carregamento do modelo para ser super rápido
@st.cache_resource
def carregar_modelo():
    """Carrega o pipeline de ML treinado (modelo + preprocessor)"""
    try:
        pipeline = joblib.load('modelo_fps.joblib')
        return pipeline
    except FileNotFoundError:
        return None

# Cacheia os CSVs para os dropdowns
@st.cache_data
def carregar_listas_dropdown():
    """Carrega os dados das nossas tabelas dimensão para os dropdowns"""
    try:
        df_cpu = pd.read_csv('dim_CPU.csv')
        df_gpu = pd.read_csv('dim_GPU.csv')
        df_jogo = pd.read_csv('dim_Jogo.csv')
        # Listas para o dropdown de qualidade/resolução
        qualidades = [
            'Baixo (Competitivo)', 'Baixo', 'Medio', 'Médio (DLSS Qualidade)', 'Médio (FSR Qualidade)',
            'Alto', 'Alto (DLSS Qualidade)', 'Alto (FSR Qualidade)', 'Muito Alto', 
            'Ultra', 'Ultra (DLSS Qualidade)', 'Ultra (FSR Qualidade)', 'Ultra (Max)',
            'Alto (DLSS Qualidade + RT)', 'Alto (FSR Qualidade + RT)'
        ]
        resolucoes = ['1080p', '1440p']

        return df_cpu, df_gpu, df_jogo, qualidades, resolucoes
    except Exception as e:
        return None, None, None, [], []

# Carregando...
ml_pipeline = carregar_modelo()
df_cpu, df_gpu, df_jogo, qualidades, resolucoes = carregar_listas_dropdown()

# --- 3. CONSTRUINDO A INTERFACE (O "SITE") ---

st.title('🖥️ Simulador de Performance (FPS) em Jogos')
st.markdown("Um projeto de Machine Learning por **Guilherme Rodrigues Almeida Rosa**")

if ml_pipeline is None or df_cpu is None:
    st.error("ERRO: O arquivo 'modelo_fps.joblib' ou os arquivos .csv não foram encontrados. Por favor, rode o script `modelo_fps.py` primeiro.")
else:
    st.success("Modelo de Machine Learning (R² 0.89) carregado com sucesso!")

    # Criando as colunas da interface
    col1, col2 = st.columns(2)

    with col1:
        st.header("Hardware (Seu PC)")
        # --- SELEÇÃO DE CPU ---
        cpu_selecionada_nome = st.selectbox(
            '1. Escolha o Processador (CPU):',
            df_cpu['nome_cpu']
        )
        # Pegar os dados (features) do CPU selecionado
        cpu_features = df_cpu[df_cpu['nome_cpu'] == cpu_selecionada_nome].iloc[0]

        # --- SELEÇÃO DE GPU ---
        gpu_selecionada_nome = st.selectbox(
            '2. Escolha a Placa de Vídeo (GPU):',
            df_gpu['nome_gpu']
        )
        # Pegar os dados (features) da GPU selecionada
        gpu_features = df_gpu[df_gpu['nome_gpu'] == gpu_selecionada_nome].iloc[0]

    with col2:
        st.header("Software (Seu Jogo)")
        # --- SELEÇÃO DE JOGO ---
        jogo_selecionado_nome = st.selectbox(
            '3. Escolha o Jogo:',
            df_jogo['nome_jogo']
        )
        # Pegar os dados (features) do Jogo selecionado
        jogo_features = df_jogo[df_jogo['nome_jogo'] == jogo_selecionado_nome].iloc[0]

        # --- SELEÇÃO DE CONFIGURAÇÕES ---
        resolucao_selecionada = st.selectbox('4. Escolha a Resolução:', resolucoes)
        qualidade_selecionada = st.selectbox('5. Escolha a Qualidade Gráfica:', qualidades)

    st.divider() # Uma linha divisória

    # --- 4. BOTÃO DE PREVISÃO E RESULTADO ---

    if st.button('Prever FPS!', type="primary", use_container_width=True):

        # 1. Montar o DataFrame de 1 linha para o modelo (o "X")
        features_para_prever = {
            'memoria_gb_gpu': gpu_features['memoria_gb'],
            'consumo_tdp_watts_gpu': gpu_features['consumo_tdp_watts'],
            'gpu_preco': gpu_features['preco_medio_brl'],
            'cpu_nucleos': cpu_features['nucleos'],
            'cpu_clock': cpu_features['clock_turbo_ghz'],
            'cpu_preco': cpu_features['preco_medio_brl'],
            'jogo_genero': jogo_features['genero'],
            'jogo_exigencia': jogo_features['nivel_exigencia_gpu'],
            'resolucao': resolucao_selecionada,
            'qualidade_grafica': qualidade_selecionada
        }
        df_para_prever = pd.DataFrame([features_para_prever])

        # 2. Fazer a previsão
        fps_previsto = ml_pipeline.predict(df_para_prever)

        # 3. Mostrar o resultado
        st.header("Resultado da Previsão:")

        col_resultado, col_info = st.columns([1, 2])

        with col_resultado:
            # O widget de métrica é perfeito para isso
            st.metric(
                label=f"FPS Médio Previsto para {jogo_selecionado_nome}",
                value=f"{fps_previsto[0]:.0f} FPS"
            )

        with col_info:
            # A sua ideia genial de mostrar o erro!
            st.info(
                "**Nota sobre a Previsão:** Este é um valor estimado pelo modelo de Machine Learning (R² 0.89). "
                "Na prática, o FPS real pode variar. **O erro médio (MAE) deste modelo é de ~28 FPS** (para mais ou para menos)."
            )