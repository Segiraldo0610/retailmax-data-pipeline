# Transformación Silver en Microsoft Fabric

La capa Silver toma las tablas Bronze y las deja listas para análisis confiable. En esta etapa convierto fechas, normalizo tipos, marco anomalías controladas y protejo datos sensibles.

## Decisión de diseño

Bronze conserva los datos casi crudos. Silver aplica reglas técnicas de limpieza y calidad sin convertir todavía el modelo en indicadores finales. Esta separación me permite explicar con claridad qué parte del pipeline recibe datos y qué parte los prepara.

Como en Bronze dejé las fechas en texto `YYYY-MM-DD` para evitar problemas de compatibilidad de Parquet con Fabric, en Silver las convierto a tipo fecha usando `to_date`.

## Tablas generadas

- `silver_mstr_proveedores`
- `silver_mstr_articulos`
- `silver_mstr_tiendas`
- `silver_crm_miembros`
- `silver_trans_ventas`
- `silver_inv_stock_diario`
- `silver_post_devoluciones`

## Reglas principales

- Convertir fechas de texto a tipo fecha.
- Convertir montos, cantidades y porcentajes a tipos numéricos.
- Normalizar textos con `trim`.
- Marcar ventas con cantidad inválida.
- Marcar descuentos extremos.
- Marcar compras de invitado.
- Proteger el correo de clientes con `email_hash` y no conservar el correo original en Silver.
- Agregar `fecha_procesamiento_silver` y `capa_datos`.

## Ejecución

1. Ejecutar primero Bronze.
2. Crear o abrir notebook `cu_02_transformacion_silver`.
3. Asociar el Lakehouse `lh_retailmax_medallion`.
4. Ejecutar `01_transformacion_silver_fabric.py`.
5. Ejecutar `02_validar_silver_fabric.py`.
