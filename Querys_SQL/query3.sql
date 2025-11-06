SELECT nome_mobo,
       chipset,
       preco_medio_brl 

FROM dim_PlacaMae
WHERE marca = 'ASUS'
AND nome_mobo LIKE '%TUF%'