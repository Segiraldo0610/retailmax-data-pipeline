# Este archivo valida conteos y reglas principales de la capa Silver.

from pyspark.sql import functions as F


CONTEOS_ESPERADOS_FULL = {
    "silver_mstr_proveedores": 800,
    "silver_mstr_articulos": 5000,
    "silver_mstr_tiendas": 150,
    "silver_crm_miembros": 50000,
    "silver_trans_ventas": 1000000,
    "silver_inv_stock_diario": 750000,
    "silver_post_devoluciones": 50000,
}


def validar_conteo(nombre_tabla, total_esperado):
    total_obtenido = spark.table(nombre_tabla).count()
    if total_obtenido != total_esperado:
        raise ValueError(
            f"{nombre_tabla}: esperaba {total_esperado:,} registros "
            f"pero encontré {total_obtenido:,}"
        )
    print(f"{nombre_tabla}: conteo correcto ({total_obtenido:,})")


def imprimir_metricas_calidad():
    ventas = spark.table("silver_trans_ventas")
    inventario = spark.table("silver_inv_stock_diario")
    clientes = spark.table("silver_crm_miembros")

    print("Métricas de calidad Silver")
    ventas.select(
        F.sum(F.col("es_cantidad_invalida").cast("int")).alias("ventas_cantidad_invalida"),
        F.sum(F.col("es_descuento_extremo").cast("int")).alias("ventas_descuento_extremo"),
        F.sum(F.col("es_compra_invitado").cast("int")).alias("ventas_invitado"),
        F.sum(F.col("es_venta_cancelada").cast("int")).alias("ventas_canceladas"),
    ).show(truncate=False)

    inventario.select(
        F.sum(F.col("es_stock_negativo").cast("int")).alias("stock_negativo"),
        F.sum(F.col("es_agotado").cast("int")).alias("registros_agotados"),
        F.sum(F.col("es_riesgo_quiebre").cast("int")).alias("registros_riesgo_quiebre"),
    ).show(truncate=False)

    clientes.select(
        F.count("*").alias("clientes"),
        F.count("email_hash").alias("clientes_con_email_hash"),
    ).show(truncate=False)


for nombre_tabla, total_esperado in CONTEOS_ESPERADOS_FULL.items():
    validar_conteo(nombre_tabla, total_esperado)

imprimir_metricas_calidad()

print("Validación Silver finalizada correctamente")
