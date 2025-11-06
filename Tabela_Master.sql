CREATE TABLE Tabela_ML_FPS AS

WITH MasterTable AS (

    SELECT t1.fps_medio,

           t2.nome_gpu,
           t2.memoria_gb AS memoria_gb_gpu,
           t2.consumo_tdp_watts AS consumo_tdp_watts_gpu,
           t2.preco_medio_brl AS gpu_preco,

           t3.nome_cpu,
           t3.nucleos AS cpu_nucleos,
           t3.clock_turbo_ghz AS cpu_clock,
           t3.preco_medio_brl AS cpu_preco,

           t4.nome_jogo,
           t4.genero AS jogo_genero,
           t4.nivel_exigencia_gpu AS jogo_exigencia,
           t1.resolucao,
           t1.qualidade_grafica

    FROM fact_Performance AS t1

    INNER JOIN dim_GPU AS t2
    ON t1.id_gpu = t2.id_gpu

    INNER JOIN dim_CPU AS t3
    ON t1.id_cpu = t3.id_cpu

    INNER JOIN dim_Jogo AS t4
    ON t1.id_jogo = t4.id_jogo
)

SELECT * FROM MasterTable;
