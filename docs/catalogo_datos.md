# Catálogo de datos

Este catálogo resume las tablas principales del proyecto, su función dentro del pipeline y los campos más relevantes. Lo uso como referencia para explicar qué datos existen, de dónde vienen y cómo se transforman entre capas.

## Fuente transaccional simulada

| Tabla | Registros full | Descripción | Campos clave |
|---|---:|---|---|
| `source.mstr_proveedores` | 800 | Proveedores de productos | `supplier_id`, `supplier_name`, `country`, `reliability_score` |
| `source.mstr_articulos` | 5.000 | Catálogo de productos | `product_id`, `sku`, `supplier_id`, `unit_cost`, `unit_price` |
| `source.mstr_tiendas` | 150 | Tiendas, canales y puntos de venta | `store_id`, `store_name`, `city`, `region`, `store_format` |
| `source.crm_miembros` | 50.000 | Clientes del programa de fidelización | `customer_id`, `member_code`, `email`, `loyalty_segment` |
| `source.trans_ventas` | 1.000.000 | Transacciones de venta | `sale_id`, `sale_date`, `store_id`, `customer_id`, `product_id`, `net_amount` |
| `source.inv_stock_diario` | 750.000 | Inventario diario por tienda y producto | `inventory_id`, `snapshot_date`, `store_id`, `product_id`, `stock_on_hand` |
| `source.post_devoluciones` | 50.000 | Devoluciones posteriores a ventas | `return_id`, `sale_id`, `return_date`, `refund_amount` |

## Capa Bronze

| Tabla | Origen | Propósito |
|---|---|---|
| `bronze_mstr_proveedores` | `mstr_proveedores.parquet` | Aterrizar proveedores sin transformaciones fuertes |
| `bronze_mstr_articulos` | `mstr_articulos.parquet` | Aterrizar catálogo de productos |
| `bronze_mstr_tiendas` | `mstr_tiendas.parquet` | Aterrizar tiendas y canales |
| `bronze_crm_miembros` | `crm_miembros.parquet` | Aterrizar clientes sintéticos |
| `bronze_trans_ventas` | `trans_ventas.parquet` | Aterrizar ventas transaccionales |
| `bronze_inv_stock_diario` | `inv_stock_diario.parquet` | Aterrizar inventario diario |
| `bronze_post_devoluciones` | `post_devoluciones.parquet` | Aterrizar devoluciones |

Campos de auditoría agregados en Bronze:

- `fecha_ingesta_bronze`;
- `tabla_origen`;
- `capa_datos`;
- `archivo_origen`;
- `modo_carga`.

## Capa Silver

| Tabla | Transformaciones principales |
|---|---|
| `silver_mstr_proveedores` | Limpieza de textos, tipos numéricos y bandera de proveedor activo |
| `silver_mstr_articulos` | Limpieza de catálogo, conversión de costos, precios y fecha de lanzamiento |
| `silver_mstr_tiendas` | Normalización de ciudad, región, formato y fecha de apertura |
| `silver_crm_miembros` | Conversión de fechas, normalización de clientes y creación de `email_hash` |
| `silver_trans_ventas` | Conversión de fechas y montos, banderas de compra invitado, venta cancelada y venta válida |
| `silver_inv_stock_diario` | Conversión de inventario, bandera de stock negativo, agotado y riesgo de quiebre |
| `silver_post_devoluciones` | Conversión de fechas, cantidades, montos y bandera de devolución válida |

Reglas de calidad principales:

- `es_cantidad_invalida`: identifica ventas con cantidad menor o igual a cero.
- `es_descuento_extremo`: identifica descuentos mayores al 80%.
- `es_venta_cancelada`: identifica órdenes canceladas.
- `es_venta_valida`: marca ventas aptas para análisis.
- `es_stock_negativo`: identifica inventario negativo.
- `es_agotado`: identifica productos sin unidades disponibles.
- `es_riesgo_quiebre`: identifica productos por debajo o cerca del punto de reorden.
- `es_devolucion_valida`: identifica devoluciones con cantidad y valor válidos.

## Capa Gold

| Tabla | Tipo | Propósito |
|---|---|---|
| `gold_dim_producto` | Dimensión | Describir productos con datos de proveedor |
| `gold_dim_tienda` | Dimensión | Describir tiendas y canales de venta |
| `gold_dim_cliente` | Dimensión | Describir clientes usando datos protegidos |
| `gold_fact_ventas` | Hecho | Consolidar eventos de venta y devoluciones |
| `gold_kpi_ventas_diarias` | KPI | Resumir ventas, descuentos y devoluciones por fecha y canal |
| `gold_kpi_inventario_diario` | KPI | Resumir disponibilidad, agotados y riesgo de quiebre |
| `gold_kpi_clientes_rfm` | KPI | Segmentar clientes por recencia, frecuencia y valor monetario |

## Datos sensibles

El dato sensible más claro del proyecto es el correo del cliente. Aunque los datos son sintéticos, decidí tratarlo como si fuera información personal. Por eso en Silver creo `email_hash` y no llevo el correo original a Gold.

Esta decisión demuestra un criterio básico de seguridad: usar identificadores protegidos cuando el dato original no es necesario para el análisis.
