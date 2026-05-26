USE riot_data;
CREATE OR REPLACE VIEW vw_meta_campeoes AS
SELECT 
    campeao,
    COUNT(*) AS total_partidas,
    SUM(CASE WHEN vitoria = 1 THEN 1 ELSE 0 END) AS vitorias,
    ROUND((SUM(CASE WHEN vitoria = 1 THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS win_rate,
    ROUND(AVG(abates), 1) AS media_abates,
    ROUND(AVG(mortes), 1) AS media_mortes,
    ROUND(AVG(assistencias), 1) AS media_assistencias,
    ROUND(AVG(dano_total), 0) AS media_dano_causado,
    ROUND(AVG(ouro_acumulado), 0) AS media_ouro_coletado 
FROM estatisticas_partidas
WHERE campeao IS NOT NULL AND campeao != ''
GROUP BY campeao
ORDER BY total_partidas DESC;

CREATE OR REPLACE VIEW vw_impacto_rotas AS
SELECT 
    rota,
    COUNT(*) AS total_jogos,
    ROUND(AVG(dano_total), 0) AS media_dano_causado,
    ROUND(AVG(ouro_acumulado), 0) AS media_ouro_coletado,
    ROUND(AVG(abates), 1) AS media_abates,
    ROUND(AVG(assistencias), 1) AS media_assistencias,
    ROUND(AVG(mortes), 1) AS media_mortes
FROM estatisticas_partidas
WHERE rota IS NOT NULL AND rota != '' AND rota != 'NONE'
GROUP BY rota
ORDER BY media_dano_causado DESC;