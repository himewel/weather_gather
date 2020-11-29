SELECT
    ((floor(((`Dim Estacoes`.`latitude` - -33.0) / 1)) * 1) + -33.0) AS `latitude`,
    ((floor(((`Dim Estacoes`.`longitude` - -61.0) / 1)) * 1) + -61.0) AS `longitude`,
    avg(`dw.fact_medicoes`.`temperatura`) AS `avg`
FROM `dw.fact_medicoes`
LEFT JOIN `dw.dim_estacoes` `Dim Estacoes`
ON `dw.fact_medicoes`.`estacoes_id` = `Dim Estacoes`.`estacoes_id`
GROUP BY `latitude`, `longitude`
ORDER BY `latitude` ASC, `longitude` ASC
