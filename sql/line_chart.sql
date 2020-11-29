SELECT
    timestamp_trunc(`dw.fact_medicoes`.`data_medicao`, month) AS `data_medicao`,
    avg(`dw.fact_medicoes`.`temperatura`) AS `avg`,
    avg(`dw.fact_medicoes`.`umidade`) AS `avg_2`
FROM `dw.fact_medicoes`
LEFT JOIN `dw.dim_estacoes` `Dim Estacoes`
ON `dw.fact_medicoes`.`estacoes_id` = `Dim Estacoes`.`estacoes_id`
GROUP BY `data_medicao`
ORDER BY `data_medicao` ASC
