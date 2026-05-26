import requests
import time
from config import RIOT_API_KEY, REGIAO_BR, REGIAO_AMERICAS

# Cabeçalho padrão de autenticação da Riot
HEADERS = {"X-Riot-Token": RIOT_API_KEY}

def _fazer_requisicao(url, delay_padrao=1.2):
    """
    Função interna (helper) para centralizar as requisições e gerenciar o Rate Limit.
    O delay_padrao de 1.2 segundos garante que faremos no máximo ~50 requisições por minuto,
    ficando bem abaixo do limite de 100 requisições a cada 2 minutos.
    """
    time.sleep(delay_padrao) # Respiro preventivo
    
    while True:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            return response.json()
            
        elif response.status_code == 429:
            tempo_espera = int(response.headers.get("Retry-After", 10))
            print(f"Rate limit atingido. Pausando extração por {tempo_espera} segundos...")
            time.sleep(tempo_espera)
            
        else:
            print(f"Erro: {response.status_code}")
            response.raise_for_status()

def buscar_puuids_challengers(top_n=20):
    url = f"https://{REGIAO_BR}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"    
    dados = _fazer_requisicao(url)
    
    # Ordena os jogadores por Pontos de Liga (League Points) do maior para o menor
    jogadores_ordenados = sorted(dados['entries'], key=lambda x: x['leaguePoints'], reverse=True)
    
    puuids = []
    # Pega apenas a quantidade definida no volume alvo
    for jogador in jogadores_ordenados[:top_n]:
        # Na versão atual da API, o PUUID já vem neste endpoint!
        puuids.append(jogador['puuid'])
        
    return puuids

def buscar_partidas_jogador(puuid, qtd=15):
    """Retorna uma lista com os IDs das últimas 'qtd' partidas de um jogador."""
    url = f"https://{REGIAO_AMERICAS}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=420&start=0&count={qtd}"
    # queue=420 garante que estamos filtrando estritamente pelas partidas Ranqueadas Solo/Duo do histórico
    return _fazer_requisicao(url)

def extrair_detalhes_partida(match_id):
    """Busca o JSON completo com os detalhes técnicos e estatísticas de uma partida específica."""
    url = f"https://{REGIAO_AMERICAS}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    return _fazer_requisicao(url)