# Este archivo está pensado para ejecutarse en un notebook de Microsoft Fabric
# asociado al Lakehouse lh_retailmax_medallion.

from pyspark.sql import functions as F


RUTA_BASE_ARCHIVOS = "Files/source_parquet"
FORMATO_ORIGEN = "parquet"
PREFIJO_TABLA_BRONZE = "bronze_"
MODO_CARGA = "overwrite_full"

TABLAS_ORIGEN = [
    "mstr_proveedores",
    "mstr_articulos",
    "mstr_tiendas",
    "crm_miembros",
    "trans_ventas",
    "inv_stock_diario",
    "post_devoluciones",
]


def construir_ruta_origen(nombre_tabla):
    return f"{RUTA_BASE_ARCHIVOS}/{nombre_tabla}.{FORMATO_ORIGEN}"


def construir_nombre_tabla_bronze(nombre_tabla):
    return f"{PREFIJO_TABLA_BRONZE}{nombre_tabla}"


def leer_archivo_origen(nombre_tabla):
    ruta_origen = construir_ruta_origen(nombre_tabla)
    return spark.read.format(FORMATO_ORIGEN).load(ruta_origen)


def agregar_metadatos_auditoria(datos, nombre_tabla):
    return (
        datos
        .withColumn("fecha_ingesta_bronze", F.current_timestamp())
        .withColumn("tabla_origen", F.lit(nombre_tabla))
        .withColumn("capa_datos", F.lit("bronze"))
        .withColumn("archivo_origen", F.input_file_name())
        .withColumn("modo_carga", F.lit(MODO_CARGA))
    )


def guardar_tabla_bronze(datos, nombre_tabla):
    nombre_tabla_bronze = construir_nombre_tabla_bronze(nombre_tabla)
    (
        datos.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(nombre_tabla_bronze)
    )
    return nombre_tabla_bronze


def cargar_tabla_bronze(nombre_tabla):
    datos_origen = leer_archivo_origen(nombre_tabla)
    datos_bronze = agregar_metadatos_auditoria(datos_origen, nombre_tabla)
    nombre_tabla_bronze = guardar_tabla_bronze(datos_bronze, nombre_tabla)
    total_registros = spark.table(nombre_tabla_bronze).count()

    print(f"{nombre_tabla_bronze}: {total_registros:,} registros cargados")


for tabla_origen in TABLAS_ORIGEN:
    cargar_tabla_bronze(tabla_origen)

print("Ingesta Bronze finalizada")
