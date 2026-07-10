# Ingesta Bronze en Microsoft Fabric

En esta etapa preparo la primera capa del Lakehouse. La capa Bronze conserva los datos de la fuente con la menor transformación posible y agrega metadatos de auditoría para poder saber cuándo y desde dónde se cargó cada tabla.

## Decisión de diseño

Para esta prueba trabajaré la capa Bronze desde archivos Parquet generados localmente en `data/source/` y cargados al Lakehouse de Microsoft Fabric en la ruta `Files/source_parquet/`.

Tomo esta decisión porque la fuente transaccional está simulada en PostgreSQL local y el ambiente de Fabric Trial puede limitar conexiones directas hacia servicios que están corriendo en mi equipo. Al usar Parquet mantengo un formato analítico, reproducible y compatible con Spark, sin perder la trazabilidad hacia la fuente original.

Durante la prueba inicial identifiqué que Fabric/Spark no leía correctamente archivos Parquet con columnas de fecha almacenadas como timestamp de alta precisión. Para evitar ese bloqueo en Bronze, dejé las fechas en formato texto `YYYY-MM-DD` dentro de los Parquet. Esta decisión mantiene el dato legible y trazable en Bronze; la conversión formal a tipo fecha queda para la capa Silver.

Las tablas Bronze se crearán en formato Delta dentro del Lakehouse con el prefijo `bronze_`. Uso prefijo en el nombre de tabla para evitar depender de una configuración específica de esquemas dentro del trial de Fabric.

## Tablas de entrada

Los archivos esperados en `Files/source_parquet/` son:

- `mstr_proveedores.parquet`
- `mstr_articulos.parquet`
- `mstr_tiendas.parquet`
- `crm_miembros.parquet`
- `trans_ventas.parquet`
- `inv_stock_diario.parquet`
- `post_devoluciones.parquet`

## Tablas Bronze generadas

El notebook crea las siguientes tablas Delta:

- `bronze_mstr_proveedores`
- `bronze_mstr_articulos`
- `bronze_mstr_tiendas`
- `bronze_crm_miembros`
- `bronze_trans_ventas`
- `bronze_inv_stock_diario`
- `bronze_post_devoluciones`

## Metadatos agregados

Cada tabla Bronze conserva las columnas originales y agrega:

- `fecha_ingesta_bronze`: fecha y hora de carga en Bronze.
- `tabla_origen`: nombre de la tabla fuente.
- `capa_datos`: valor fijo `bronze`.
- `archivo_origen`: ruta del archivo leído por Spark.
- `modo_carga`: valor fijo `overwrite_dev`, usado durante el desarrollo para permitir ejecuciones repetibles.

## Ejecución esperada

1. Abrir el workspace `ws_retailmax_data_dev`.
2. Abrir el Lakehouse `lh_retailmax_medallion`.
3. Cargar los archivos Parquet locales de `data/fabric_upload/source/` en `Files/source_parquet/`.
4. Crear o abrir un notebook de Fabric asociado al Lakehouse.
5. Ejecutar el contenido de `01_ingesta_bronze_fabric.py`.
6. Ejecutar `02_validar_bronze_fabric.py` para revisar conteos.
7. Tomar evidencia de las tablas creadas y de la salida de validación.

## Conteos esperados en modo dev

| Tabla | Registros esperados |
|---|---:|
| `bronze_mstr_proveedores` | 80 |
| `bronze_mstr_articulos` | 500 |
| `bronze_mstr_tiendas` | 30 |
| `bronze_crm_miembros` | 3.000 |
| `bronze_trans_ventas` | 30.000 |
| `bronze_inv_stock_diario` | 40.000 |
| `bronze_post_devoluciones` | 1.500 |

## Evidencias sugeridas

Para sustentar esta etapa guardaré evidencia de:

- archivos cargados en `Files/source_parquet/`;
- tablas Bronze creadas en el Lakehouse;
- salida del notebook con conteos por tabla;
- consulta SQL o Spark mostrando los registros de una tabla Bronze.
