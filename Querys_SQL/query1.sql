SELECT nome_gpu,
       marca,
       preco_medio_brl

FROM dim_GPU
WHERE marca = 'NVIDIA'