import pandas as pd

def transformar_dados_partida(dados_json, match_id):

    dados_limpos = []
        
    for jogador in dados_json['info']['participants']:        
        nome_jogador = jogador.get("riotIdGameName", jogador.get("summonerName", "Desconhecido"))
        
        dados_limpos.append({
            "match_id": match_id,
            "puuid": jogador.get("puuid"),
            "nome_jogador": nome_jogador,               
            "campeao": jogador.get("championName"),
            "rota": jogador.get("teamPosition"),
            "vitoria": jogador.get("win"),
            "abates": jogador.get("kills"),
            "mortes": jogador.get("deaths"),
            "assistencias": jogador.get("assists"),
            "dano_total": jogador.get("totalDamageDealtToChampions"),
            "ouro_acumulado": jogador.get("goldEarned")
        })
        
    return pd.DataFrame(dados_limpos)