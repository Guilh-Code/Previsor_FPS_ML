# %%

import pandas as pd
import sqlite3
import os

# --- CONFIGURAÇÃO ---

# 1. O nome que seu banco de dados terá
DB_NAME = 'pc_analytics.db'

# 2. A lista exata dos 10 arquivos CSV que você criou
#    (Usei os nomes que você atualizou, como 'dim_PlacaMae' e 'dim_Fonte')
CSV_FILES = [
    'dim_CPU.csv',
    'dim_GPU.csv',
    'dim_PlacaMae.csv',
    'dim_RAM.csv',
    'dim_Storage.csv',
    'dim_Fonte.csv',
    'dim_Cooler.csv',
    'dim_Gabinete.csv',
    'dim_Jogo.csv',
    'fact_Performance.csv'
]

# --- FIM DA CONFIGURAÇÃO ---


def criar_banco_de_dados():
    """
    Lê todos os arquivos CSV da lista CSV_FILES e os importa como tabelas
    em um novo banco de dados SQLite.
    """
    
    print(f"Iniciando a criação do banco de dados: {DB_NAME}...")
    
    # Deleta o banco de dados antigo, se existir, para começar do zero
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f"Banco de dados antigo '{DB_NAME}' removido.")

    # Conecta ao banco de dados (ele será criado agora)
    conn = sqlite3.connect(DB_NAME)
    
    try:
        total_arquivos = len(CSV_FILES)
        for i, csv_file in enumerate(CSV_FILES, 1):
            
            # Pega o nome do arquivo sem a extensão .csv para usar como nome da tabela
            # Ex: "dim_CPU.csv" -> "dim_CPU"
            table_name = os.path.splitext(csv_file)[0]
            
            print(f"[{i}/{total_arquivos}] Processando arquivo: {csv_file}  -> Tabela: {table_name}")
            
            # Lê o arquivo CSV para um DataFrame do Pandas
            df = pd.read_csv(csv_file)
            
            # Salva o DataFrame no banco de dados SQLite
            # if_exists='replace': Cria uma nova tabela (já que apagamos o .db)
            # index=False: Não salva o índice do DataFrame (0, 1, 2...) como uma coluna.
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            
        print(f"\n--- SUCESSO! ---")
        print(f"Todas as {total_arquivos} tabelas foram importadas para o banco de dados '{DB_NAME}'.")
        
    except FileNotFoundError as e:
        print(f"\n[ERRO CRÍTICO] Arquivo não encontrado: {e.filename}")
        print("Por favor, verifique se o nome do arquivo está correto na lista CSV_FILES")
        print("e se todos os 10 arquivos .csv estão na MESMA PASTA que este script.")
    except Exception as e:
        print(f"\n[ERRO] Ocorreu um erro inesperado: {e}")
        
    finally:
        # Fecha a conexão com o banco de dados
        conn.close()
        print("Conexão com o banco de dados fechada.")

# Esta é a linha padrão que executa a função principal quando você roda o script
if __name__ == "__main__":
    criar_banco_de_dados()

# %%
