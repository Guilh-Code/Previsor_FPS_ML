WITH Custo_Beneficio_Mais100FPS AS (

    SELECT t2.nome_gpu,
        t2.preco_medio_brl,
        ROUND(AVG(t1.fps_medio), 2) AS fps_medio,
        ROUND(t2.preco_medio_brl / AVG(t1.fps_medio), 2) AS Custo_Beneficio_Medio_1080p

    FROM fact_Performance AS t1

    INNER JOIN dim_GPU AS t2
    ON t1.id_gpu = t2.id_gpu

    INNER JOIN dim_Jogo AS t3
    ON t1.id_jogo = t3.id_jogo

    WHERE t3.nome_jogo IN ('Cyberpunk 2077', 'Alan Wake 2', 'Elden Ring', 'Starfield', 'Red Dead Redemption 2', 'Forza Horizon 5', "Baldur's Gate 3")
    AND t1.qualidade_grafica IN ('Alto', 'Alto (DLSS Qualidade)', 'Alto (FSR Qualidade)')
    AND t1.resolucao = '1080p'

    GROUP BY t2.nome_gpu, t2.preco_medio_brl

    ORDER BY Custo_Beneficio_Medio_1080p
)

SELECT *
FROM Custo_Beneficio_Mais100FPS
WHERE fps_medio > 100