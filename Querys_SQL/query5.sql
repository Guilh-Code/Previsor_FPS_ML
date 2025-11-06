SELECT marca,
       ROUND(AVG(preco_medio_brl), 2) AS MediaPreco

FROM dim_GPU
GROUP BY marca
ORDER BY MediaPreco