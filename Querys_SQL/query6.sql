SELECT a.nome_cpu,
       b.nome_mobo     

FROM dim_CPU AS a

INNER JOIN dim_PlacaMae AS b
ON a.socket = b.socket_compativel

WHERE a.socket = 'AM5'
