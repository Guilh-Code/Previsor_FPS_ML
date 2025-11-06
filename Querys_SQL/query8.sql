SELECT t3.nome_jogo,
       t1.qualidade_grafica,
       t1.fps_medio     

FROM fact_Performance AS t1

INNER JOIN dim_GPU AS t2
ON t1.id_gpu = t2.id_gpu

INNER JOIN dim_Jogo AS t3
ON t1.id_jogo = t3.id_jogo

WHERE t2.nome_gpu = 'RX 7600'

ORDER BY t1.fps_medio