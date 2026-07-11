# Modelo Gold en Microsoft Fabric

La capa Gold convierte los datos limpios de Silver en tablas orientadas al análisis de negocio. En esta prueba priorizo ventas, devoluciones, inventario y clientes.

## Decisión de diseño

Gold no conserva todas las columnas operativas. Se concentra en dimensiones, hechos y KPIs que responden preguntas de negocio:

- cuánto se vendió;
- cuánto se devolvió;
- qué productos o tiendas tienen mayor movimiento;
- dónde hay riesgo de quiebre de stock;
- cómo se comportan los clientes registrados.

## Tablas generadas

- `gold_dim_producto`
- `gold_dim_tienda`
- `gold_dim_cliente`
- `gold_fact_ventas`
- `gold_kpi_ventas_diarias`
- `gold_kpi_inventario_diario`
- `gold_kpi_clientes_rfm`

## Reglas principales

- El hecho de ventas conserva todas las ventas, pero calcula métricas analíticas principalmente sobre ventas válidas y no canceladas.
- Las devoluciones se agregan por `sale_id` y se descuentan de la venta neta.
- El inventario se resume por fecha y tienda.
- El análisis RFM usa clientes registrados con compras válidas.

## Ejecución

1. Ejecutar Bronze.
2. Ejecutar Silver.
3. Crear o abrir notebook `cu_03_modelo_gold`.
4. Asociar el Lakehouse `lh_retailmax_medallion`.
5. Ejecutar `01_modelo_gold_fabric.py`.
6. Ejecutar `02_validar_gold_fabric.py`.
