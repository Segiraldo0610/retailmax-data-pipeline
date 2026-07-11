SELECT *
FROM (
    SELECT 1 AS orden, 'mstr_proveedores' AS tabla, COUNT(*) AS registros FROM source.mstr_proveedores
    UNION ALL
    SELECT 2 AS orden, 'mstr_articulos' AS tabla, COUNT(*) AS registros FROM source.mstr_articulos
    UNION ALL
    SELECT 3 AS orden, 'mstr_tiendas' AS tabla, COUNT(*) AS registros FROM source.mstr_tiendas
    UNION ALL
    SELECT 4 AS orden, 'crm_miembros' AS tabla, COUNT(*) AS registros FROM source.crm_miembros
    UNION ALL
    SELECT 5 AS orden, 'trans_ventas' AS tabla, COUNT(*) AS registros FROM source.trans_ventas
    UNION ALL
    SELECT 6 AS orden, 'inv_stock_diario' AS tabla, COUNT(*) AS registros FROM source.inv_stock_diario
    UNION ALL
    SELECT 7 AS orden, 'post_devoluciones' AS tabla, COUNT(*) AS registros FROM source.post_devoluciones
) conteos
ORDER BY orden;
