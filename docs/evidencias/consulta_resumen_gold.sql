SELECT
    COUNT(*) AS ventas_totales,
    SUM(CASE WHEN es_venta_valida THEN 1 ELSE 0 END) AS ventas_validas,
    ROUND(SUM(net_amount_analitico), 2) AS venta_neta,
    ROUND(SUM(refund_amount_total), 2) AS devoluciones,
    ROUND(SUM(net_amount_after_returns), 2) AS venta_neta_despues_devoluciones
FROM gold_fact_ventas;

SELECT
    COUNT(*) AS dias_canales_con_venta,
    ROUND(SUM(venta_neta), 2) AS venta_neta,
    ROUND(SUM(devoluciones_valor), 2) AS devoluciones_valor,
    ROUND(SUM(venta_neta_despues_devoluciones), 2) AS venta_neta_despues_devoluciones
FROM gold_kpi_ventas_diarias;

SELECT
    SUM(productos_agotados) AS productos_agotados,
    SUM(productos_riesgo_quiebre) AS productos_riesgo_quiebre
FROM gold_kpi_inventario_diario;
