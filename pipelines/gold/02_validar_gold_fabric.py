# Este archivo valida conteos y KPIs principales de la capa Gold.

from pyspark.sql import functions as F


CONTEOS_MINIMOS = {
    "gold_dim_producto": 500,
    "gold_dim_tienda": 30,
    "gold_dim_cliente": 3000,
    "gold_fact_ventas": 30000,
    "gold_kpi_ventas_diarias": 1,
    "gold_kpi_inventario_diario": 1,
    "gold_kpi_clientes_rfm": 1,
}


def validar_minimo(nombre_tabla, minimo_esperado):
    total_obtenido = spark.table(nombre_tabla).count()
    if total_obtenido < minimo_esperado:
        raise ValueError(
            f"{nombre_tabla}: esperaba al menos {minimo_esperado:,} registros "
            f"pero encontré {total_obtenido:,}"
        )
    print(f"{nombre_tabla}: validación correcta ({total_obtenido:,} registros)")


for nombre_tabla, minimo_esperado in CONTEOS_MINIMOS.items():
    validar_minimo(nombre_tabla, minimo_esperado)


print("Resumen de KPIs Gold")

spark.table("gold_fact_ventas").select(
    F.count("*").alias("ventas_totales"),
    F.sum(F.col("es_venta_valida").cast("int")).alias("ventas_validas"),
    F.round(F.sum("net_amount_analitico"), 2).alias("venta_neta"),
    F.round(F.sum("refund_amount_total"), 2).alias("devoluciones"),
    F.round(F.sum("net_amount_after_returns"), 2).alias("venta_neta_despues_devoluciones"),
).show(truncate=False)

spark.table("gold_kpi_inventario_diario").select(
    F.sum("productos_agotados").alias("productos_agotados"),
    F.sum("productos_riesgo_quiebre").alias("productos_riesgo_quiebre"),
).show(truncate=False)

print("Validación Gold finalizada correctamente")
