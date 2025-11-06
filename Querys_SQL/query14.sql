SELECT t2.nome_gpu,
       t2.preco_medio_brl,
       ROUND(AVG(t1.fps_medio), 2) AS fps_medio,
       ROUND(t2.preco_medio_brl / AVG(t1.fps_medio), 2) AS Custo_Beneficio_Medio_1080p

FROM fact_Performance AS t1

INNER JOIN dim_GPU AS t2
ON t1.id_gpu = t2.id_gpu

INNER JOIN dim_Jogo AS t3
ON t1.id_jogo = t3.id_jogo

WHERE t3.nome_jogo IN ('Valorant', 'Counter-Strike 2', 'League of Legends', 'Apex Legends', 'Rainbow Six Siege', 'Rocket League')
AND t1.qualidade_grafica IN ('Baixo (Competitivo)', 'Muito Alto')
AND t1.resolucao = '1080p'

GROUP BY t2.nome_gpu, t2.preco_medio_brl
ORDER BY Custo_Beneficio_Medio_1080p