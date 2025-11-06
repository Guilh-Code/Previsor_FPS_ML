SELECT nome_cpu,
       nome_mobo,
       nome_ram 

FROM dim_CPU AS a

INNER JOIN dim_PlacaMae AS b
ON a.socket = b.socket_compativel

INNER JOIN dim_RAM AS c
ON b.tipo_ram_suportado = c.tipo_ram

WHERE a.nome_cpu = 'Ryzen 5 7600'