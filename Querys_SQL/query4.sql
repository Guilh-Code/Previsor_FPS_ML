SELECT socket,
       count(*) AS Qtde

FROM dim_CPU
GROUP BY socket