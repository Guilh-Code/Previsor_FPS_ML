SELECT t2.nome_cpu,
       t3.nome_gpu,
       t4.nome_jogo,
       t1.qualidade_grafica,
       t1.fps_medio 

FROM fact_Performance AS t1

INNER JOIN dim_CPU AS t2
ON t1.id_cpu = t2.id_cpu

INNER JOIN dim_GPU AS t3
ON t1.id_gpu = t3.id_gpu

INNER JOIN dim_Jogo AS t4
ON t1.id_jogo = t4.id_jogo

WHERE t3.nome_gpu = 'RX 7600'
AND t4.nome_jogo = 'Cyberpunk 2077'

ORDER BY t1.fps_medio