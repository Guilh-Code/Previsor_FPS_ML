SELECT nome_cpu,
       socket,
       nucleos,
       preco_medio_brl 

FROM dim_CPU
WHERE preco_medio_brl <= 1500
ORDER BY preco_medio_brl
