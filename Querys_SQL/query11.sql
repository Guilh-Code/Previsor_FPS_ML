SELECT t2.nome_gpu,
       t2.preco_medio_brl,
       ROUND(AVG(t1.fps_medio), 2) AS fps_medio,
       ROUND(t2.preco_medio_brl / AVG(t1.fps_medio), 2) AS Custo_Beneficio_Medio_1080p   

FROM fact_Performance AS t1

INNER JOIN dim_GPU AS t2
ON t1.id_gpu = t2.id_gpu

WHERE t1.resolucao = '1080p'

GROUP BY t2.nome_gpu
ORDER BY Custo_Beneficio_Medio_1080p