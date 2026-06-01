import pandas as pd
from sqlalchemy import create_engine
from config import DATABASE_URI

def carregar_dados_mysql(df_partida, nome_tabela="estatisticas_partidas"):
    if df_partida.empty:
        print("df vazio")
        return False
        
    print(f"inserindo {len(df_partida)} linhas no MySQL...")
    
    try:
        engine = create_engine(DATABASE_URI)        
        df_partida.to_sql(nome_tabela, con=engine, if_exists='append', index=False)
        
        print("\n dados inseridos na tabela")
        return True
        
    except Exception as e:
        print(f"Erro ao conectar ou inserir no banco de dados: {e}")
        return False
    
def buscar_partidas_existentes():
    """Busca no MySQL os IDs das partidas que já foram processadas."""
    print("Verificando histórico no banco de dados...")
    try:
        engine = create_engine(DATABASE_URI)
        df = pd.read_sql("SELECT DISTINCT match_id FROM estatisticas_partidas", engine)
        ids_existentes = set(df['match_id'].tolist())
        print(f"✅ {len(ids_existentes)} partidas anteriores carregadas na memória.")
        return ids_existentes
        
    except Exception as e:
        print(f"Erro ao buscar histórico: {e}. Iniciando com lista vazia.")
        return set()