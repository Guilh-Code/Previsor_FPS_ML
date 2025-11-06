SELECT t1.nome_cooler,
       t1.altura_cooler_mm,
       t2.nome_case,
       t2.limite_altura_aircooler_mm

FROM dim_Cooler AS t1

INNER JOIN dim_Gabinete AS t2
ON t1.tamanho_radiador_mm <= t2.suporte_radiador_topo_mm

WHERE t2.nome_case = 'Lian Li Vector V100'
AND t1.tipo_cooler = 'Water Cooler'