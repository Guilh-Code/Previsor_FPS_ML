SELECT t2.nome_gpu,
       t1.fps_medio,
       t2.preco_medio_brl,
       ROUND(t2.preco_medio_brl / t1.fps_medio, 2) AS Custo_por_FPS

FROM fact_Performance AS t1

INNER JOIN dim_GPU AS t2
ON t1.id_gpu = t2.id_gpu

INNER JOIN dim_Jogo AS t3
ON t1.id_jogo = t3.id_jogo

WHERE t3.nome_jogo = 'Cyberpunk 2077'
AND t1.qualidade_grafica = 'Alto'
AND t1.resolucao = '1080p'

ORDER BY Custo_por_FPS
