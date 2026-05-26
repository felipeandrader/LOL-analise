USE riot_data;

CREATE TABLE estatisticas_partidas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    match_id VARCHAR(25),
    puuid VARCHAR(100),
    nome_jogador VARCHAR(100),
    campeao VARCHAR(50),
    rota VARCHAR(30),
    vitoria BOOLEAN,
    abates INT,
    mortes INT,
    assistencias INT,
    dano_total INT,
    ouro_acumulado INT
);