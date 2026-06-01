import time
from etl.extractor import buscar_puuids_challengers, buscar_partidas_jogador, extrair_detalhes_partida
from etl.transformer import transformar_dados_partida
from etl.loader import carregar_dados_mysql, buscar_partidas_existentes

TOP_N_JOGADORES = 20
PARTIDAS_POR_JOGADOR = 15

def executar_pipeline_etl():
    print("INICIANDO PIPELINE ETL - PROJETO DADOS LOL\n")
    tempo_inicio = time.time()
    partidas_processadas = buscar_partidas_existentes()
    total_linhas_inseridas = 0
    
    try:
        puuids = buscar_puuids_challengers(top_n=TOP_N_JOGADORES)
        print(f"Encontrados {len(puuids)} jogadores Challenger.")
        
        for i, puuid in enumerate(puuids, start=1):
            print(f"\n[{i}/{len(puuids)}] Buscando partidas para o jogador...")
            
            partidas = buscar_partidas_jogador(puuid, qtd=PARTIDAS_POR_JOGADOR)
            
            for match_id in partidas:
                if match_id in partidas_processadas:
                    print(f"Partida {match_id} já processada anteriormente. Pulando...")
                    continue
                
                print(f"Processando partida: {match_id}")
                
                json_bruto = extrair_detalhes_partida(match_id)
                df_partida = transformar_dados_partida(json_bruto, match_id)
                sucesso = carregar_dados_mysql(df_partida)
                
                if sucesso:
                    partidas_processadas.add(match_id)
                    total_linhas_inseridas += len(df_partida)
                    
    except Exception as e:
        print(f"\nERRO CRÍTICO NO PIPELINE: {e}")
        
    finally:
        tempo_total = time.time() - tempo_inicio
        print("PIPELINE FINALIZADO")
        print(f"Partidas unicas processadas: {len(partidas_processadas)}")
        print(f"Total de linhas no banco: {total_linhas_inseridas}")
        print(f"Tempo de execução: {tempo_total:.2f} segundos")

if __name__ == "__main__":
    executar_pipeline_etl()