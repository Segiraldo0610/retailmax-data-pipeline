# Este archivo está pensado para ejecutarse en un notebook de Microsoft Fabric
# asociado al Lakehouse lh_retailmax_medallion.

from pyspark.sql import functions as F


MODO_ESCRITURA = "overwrite"


def guardar_tabla_gold(datos, nombre_tabla):
    (
        datos.write
        .format("delta")
        .mode(MODO_ESCRITURA)
        .option("overwriteSchema", "true")
        .saveAsTable(nombre_tabla)
    )
    print(f"{nombre_tabla}: {spark.table(nombre_tabla).count():,} registros")


def agregar_auditoria_gold(datos):
    return (
        datos
        .withColumn("fecha_procesamiento_gold", F.current_timestamp())
        .withColumn("capa_datos", F.lit("gold"))
    )


proveedores = spark.table("silver_mstr_proveedores")
articulos = spark.table("silver_mstr_articulos")
tiendas = spark.table("silver_mstr_tiendas")
clientes = spark.table("silver_crm_miembros")
ventas = spark.table("silver_trans_ventas")
inventario = spark.table("silver_inv_stock_diario")
devoluciones = spark.table("silver_post_devoluciones")


gold_dim_producto = (
    articulos.alias("p")
    .join(proveedores.alias("s"), F.col("p.supplier_id") == F.col("s.supplier_id"), "left")
    .select(
        F.col("p.product_id"),
        F.col("p.sku"),
        F.col("p.product_name"),
        F.col("p.category"),
        F.col("p.subcategory"),
        F.col("p.brand"),
        F.col("p.supplier_id"),
        F.col("s.supplier_name"),
        F.col("s.country").alias("supplier_country"),
        F.col("p.unit_cost"),
        F.col("p.unit_price"),
        F.col("p.launch_date"),
        F.col("p.is_active").alias("product_is_active"),
    )
)


gold_dim_tienda = tiendas.select(
    "store_id",
    "store_name",
    "city",
    "region",
    "store_format",
    "opening_date",
    F.col("is_active").alias("store_is_active"),
)


gold_dim_cliente = (
    clientes
    .withColumn("edad_aproximada", F.floor(F.months_between(F.current_date(), F.col("birth_date")) / 12))
    .select(
        "customer_id",
        "member_code",
        "first_name",
        "last_name",
        "gender",
        "birth_date",
        "edad_aproximada",
        "city",
        "loyalty_segment",
        "registration_date",
        "email_hash",
    )
)


devoluciones_por_venta = (
    devoluciones
    .filter(F.col("es_devolucion_valida"))
    .groupBy("sale_id")
    .agg(
        F.sum("returned_quantity").alias("returned_quantity_total"),
        F.sum("refund_amount").alias("refund_amount_total"),
        F.count("*").alias("return_events"),
    )
)


gold_fact_ventas = (
    ventas.alias("v")
    .join(devoluciones_por_venta.alias("d"), "sale_id", "left")
    .withColumn("returned_quantity_total", F.coalesce(F.col("returned_quantity_total"), F.lit(0)))
    .withColumn("refund_amount_total", F.coalesce(F.col("refund_amount_total"), F.lit(0.0)))
    .withColumn("return_events", F.coalesce(F.col("return_events"), F.lit(0)))
    .withColumn("tiene_devolucion", F.col("return_events") > 0)
    .withColumn(
        "net_amount_after_returns",
        F.when(
            F.col("es_venta_valida") & (~F.col("es_venta_cancelada")),
            F.col("net_amount") - F.col("refund_amount_total"),
        ).otherwise(F.lit(0.0)),
    )
    .withColumn(
        "net_amount_analitico",
        F.when(F.col("es_venta_valida") & (~F.col("es_venta_cancelada")), F.col("net_amount")).otherwise(F.lit(0.0)),
    )
    .select(
        "sale_id",
        "sale_date",
        "store_id",
        "customer_id",
        "product_id",
        "channel",
        "quantity",
        "unit_price",
        "discount_rate",
        "gross_amount",
        "discount_amount",
        "net_amount",
        "refund_amount_total",
        "net_amount_analitico",
        "net_amount_after_returns",
        "payment_method",
        "order_status",
        "es_compra_invitado",
        "es_venta_valida",
        "es_venta_cancelada",
        "tiene_devolucion",
    )
)


gold_kpi_ventas_diarias = (
    gold_fact_ventas
    .groupBy("sale_date", "channel")
    .agg(
        F.count("*").alias("ordenes_totales"),
        F.sum(F.when(F.col("es_venta_valida") & (~F.col("es_venta_cancelada")), 1).otherwise(0)).alias("ordenes_validas"),
        F.sum(F.when(F.col("es_venta_valida") & (~F.col("es_venta_cancelada")), F.col("quantity")).otherwise(0)).alias("unidades_vendidas"),
        F.round(F.sum("gross_amount"), 2).alias("venta_bruta"),
        F.round(F.sum("discount_amount"), 2).alias("descuento_total"),
        F.round(F.sum("net_amount_analitico"), 2).alias("venta_neta"),
        F.round(F.sum("refund_amount_total"), 2).alias("devoluciones_valor"),
        F.round(F.sum("net_amount_after_returns"), 2).alias("venta_neta_despues_devoluciones"),
    )
)


gold_kpi_inventario_diario = (
    inventario
    .groupBy("snapshot_date", "store_id")
    .agg(
        F.countDistinct("product_id").alias("productos_monitoreados"),
        F.sum("stock_on_hand").alias("unidades_disponibles"),
        F.sum(F.col("es_agotado").cast("int")).alias("productos_agotados"),
        F.sum(F.col("es_riesgo_quiebre").cast("int")).alias("productos_riesgo_quiebre"),
    )
)


fecha_referencia = gold_fact_ventas.agg(F.max("sale_date").alias("fecha_referencia"))

gold_kpi_clientes_rfm = (
    gold_fact_ventas
    .filter(
        F.col("customer_id").isNotNull()
        & F.col("es_venta_valida")
        & (~F.col("es_venta_cancelada"))
    )
    .groupBy("customer_id")
    .agg(
        F.max("sale_date").alias("ultima_compra"),
        F.countDistinct("sale_id").alias("frecuencia_compra"),
        F.round(F.sum("net_amount_after_returns"), 2).alias("valor_monetario"),
    )
    .crossJoin(fecha_referencia)
    .withColumn("recencia_dias", F.datediff(F.col("fecha_referencia"), F.col("ultima_compra")))
    .join(gold_dim_cliente.select("customer_id", "loyalty_segment", "city"), "customer_id", "left")
)


TABLAS_GOLD = {
    "gold_dim_producto": agregar_auditoria_gold(gold_dim_producto),
    "gold_dim_tienda": agregar_auditoria_gold(gold_dim_tienda),
    "gold_dim_cliente": agregar_auditoria_gold(gold_dim_cliente),
    "gold_fact_ventas": agregar_auditoria_gold(gold_fact_ventas),
    "gold_kpi_ventas_diarias": agregar_auditoria_gold(gold_kpi_ventas_diarias),
    "gold_kpi_inventario_diario": agregar_auditoria_gold(gold_kpi_inventario_diario),
    "gold_kpi_clientes_rfm": agregar_auditoria_gold(gold_kpi_clientes_rfm),
}


for nombre_tabla, datos_tabla in TABLAS_GOLD.items():
    guardar_tabla_gold(datos_tabla, nombre_tabla)

print("Modelo Gold finalizado")
