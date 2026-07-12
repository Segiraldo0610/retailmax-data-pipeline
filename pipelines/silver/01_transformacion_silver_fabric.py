from pyspark.sql import functions as F


MODO_ESCRITURA = "overwrite"


def leer_tabla_bronze(nombre_tabla):
    return spark.table(f"bronze_{nombre_tabla}")


def normalizar_textos(datos, columnas):
    for columna in columnas:
        datos = datos.withColumn(columna, F.trim(F.col(columna)))
    return datos


def agregar_auditoria_silver(datos):
    return (
        datos
        .withColumn("fecha_procesamiento_silver", F.current_timestamp())
        .withColumn("capa_datos", F.lit("silver"))
    )


def guardar_tabla_silver(datos, nombre_tabla):
    (
        datos.write
        .format("delta")
        .mode(MODO_ESCRITURA)
        .option("overwriteSchema", "true")
        .saveAsTable(nombre_tabla)
    )
    print(f"{nombre_tabla}: {spark.table(nombre_tabla).count():,} registros")


def transformar_proveedores():
    datos = leer_tabla_bronze("mstr_proveedores").select(
        "supplier_id",
        "supplier_name",
        "country",
        "category_specialty",
        "lead_time_days",
        "reliability_score",
        "is_active",
    )
    datos = normalizar_textos(datos, ["supplier_id", "supplier_name", "country", "category_specialty"])
    datos = (
        datos
        .withColumn("lead_time_days", F.col("lead_time_days").cast("int"))
        .withColumn("reliability_score", F.col("reliability_score").cast("double"))
        .withColumn("is_active", F.col("is_active").cast("boolean"))
    )
    return agregar_auditoria_silver(datos)


def transformar_articulos():
    datos = leer_tabla_bronze("mstr_articulos").select(
        "product_id",
        "sku",
        "product_name",
        "category",
        "subcategory",
        "brand",
        "supplier_id",
        "unit_cost",
        "unit_price",
        "launch_date",
        "is_active",
    )
    datos = normalizar_textos(
        datos,
        ["product_id", "sku", "product_name", "category", "subcategory", "brand", "supplier_id"],
    )
    datos = (
        datos
        .withColumn("unit_cost", F.col("unit_cost").cast("double"))
        .withColumn("unit_price", F.col("unit_price").cast("double"))
        .withColumn("launch_date", F.to_date("launch_date", "yyyy-MM-dd"))
        .withColumn("is_active", F.col("is_active").cast("boolean"))
    )
    return agregar_auditoria_silver(datos)


def transformar_tiendas():
    datos = leer_tabla_bronze("mstr_tiendas").select(
        "store_id",
        "store_name",
        "city",
        "region",
        "store_format",
        "opening_date",
        "is_active",
    )
    datos = normalizar_textos(datos, ["store_id", "store_name", "city", "region", "store_format"])
    datos = (
        datos
        .withColumn("opening_date", F.to_date("opening_date", "yyyy-MM-dd"))
        .withColumn("is_active", F.col("is_active").cast("boolean"))
    )
    return agregar_auditoria_silver(datos)


def transformar_clientes():
    datos = leer_tabla_bronze("crm_miembros").select(
        "customer_id",
        "member_code",
        "first_name",
        "last_name",
        "email",
        "gender",
        "birth_date",
        "city",
        "loyalty_segment",
        "registration_date",
    )
    datos = normalizar_textos(
        datos,
        ["customer_id", "member_code", "first_name", "last_name", "email", "gender", "city", "loyalty_segment"],
    )
    datos = (
        datos
        .withColumn("birth_date", F.to_date("birth_date", "yyyy-MM-dd"))
        .withColumn("registration_date", F.to_date("registration_date", "yyyy-MM-dd"))
        .withColumn("email_hash", F.sha2(F.lower(F.col("email")), 256))
        .drop("email")
    )
    return agregar_auditoria_silver(datos)


def transformar_ventas():
    datos = leer_tabla_bronze("trans_ventas").select(
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
        "payment_method",
        "order_status",
    )
    datos = normalizar_textos(
        datos,
        ["sale_id", "store_id", "customer_id", "product_id", "channel", "payment_method", "order_status"],
    )
    datos = (
        datos
        .withColumn("customer_id", F.when(F.col("customer_id") == "", None).otherwise(F.col("customer_id")))
        .withColumn("sale_date", F.to_date("sale_date", "yyyy-MM-dd"))
        .withColumn("quantity", F.col("quantity").cast("int"))
        .withColumn("unit_price", F.col("unit_price").cast("double"))
        .withColumn("discount_rate", F.col("discount_rate").cast("double"))
        .withColumn("gross_amount", F.col("gross_amount").cast("double"))
        .withColumn("discount_amount", F.col("discount_amount").cast("double"))
        .withColumn("net_amount", F.col("net_amount").cast("double"))
        .withColumn("es_compra_invitado", F.col("customer_id").isNull())
        .withColumn("es_cantidad_invalida", F.col("quantity") <= 0)
        .withColumn("es_descuento_extremo", F.col("discount_rate") > 0.80)
        .withColumn("es_venta_cancelada", F.col("order_status") == "cancelada")
        .withColumn(
            "es_venta_valida",
            (F.col("quantity") > 0)
            & (F.col("discount_rate").between(0, 0.80))
            & (F.col("net_amount") >= 0)
            & F.col("store_id").isNotNull()
            & F.col("product_id").isNotNull(),
        )
    )
    return agregar_auditoria_silver(datos)


def transformar_inventario():
    datos = leer_tabla_bronze("inv_stock_diario").select(
        "inventory_id",
        "snapshot_date",
        "store_id",
        "product_id",
        "stock_on_hand",
        "reorder_point",
        "safety_stock",
        "stock_status",
    )
    datos = normalizar_textos(datos, ["inventory_id", "store_id", "product_id", "stock_status"])
    datos = (
        datos
        .withColumn("snapshot_date", F.to_date("snapshot_date", "yyyy-MM-dd"))
        .withColumn("stock_on_hand", F.col("stock_on_hand").cast("int"))
        .withColumn("reorder_point", F.col("reorder_point").cast("int"))
        .withColumn("safety_stock", F.col("safety_stock").cast("int"))
        .withColumn("es_stock_negativo", F.col("stock_on_hand") < 0)
        .withColumn("es_agotado", F.col("stock_on_hand") == 0)
        .withColumn("es_riesgo_quiebre", F.col("stock_on_hand") <= F.col("reorder_point"))
    )
    return agregar_auditoria_silver(datos)


def transformar_devoluciones():
    datos = leer_tabla_bronze("post_devoluciones").select(
        "return_id",
        "sale_id",
        "return_date",
        "store_id",
        "customer_id",
        "product_id",
        "returned_quantity",
        "return_reason",
        "refund_amount",
        "return_channel",
    )
    datos = normalizar_textos(
        datos,
        ["return_id", "sale_id", "store_id", "customer_id", "product_id", "return_reason", "return_channel"],
    )
    datos = (
        datos
        .withColumn("customer_id", F.when(F.col("customer_id") == "", None).otherwise(F.col("customer_id")))
        .withColumn("return_date", F.to_date("return_date", "yyyy-MM-dd"))
        .withColumn("returned_quantity", F.col("returned_quantity").cast("int"))
        .withColumn("refund_amount", F.col("refund_amount").cast("double"))
        .withColumn("es_devolucion_valida", (F.col("returned_quantity") > 0) & (F.col("refund_amount") >= 0))
    )
    return agregar_auditoria_silver(datos)


TABLAS_SILVER = {
    "silver_mstr_proveedores": transformar_proveedores(),
    "silver_mstr_articulos": transformar_articulos(),
    "silver_mstr_tiendas": transformar_tiendas(),
    "silver_crm_miembros": transformar_clientes(),
    "silver_trans_ventas": transformar_ventas(),
    "silver_inv_stock_diario": transformar_inventario(),
    "silver_post_devoluciones": transformar_devoluciones(),
}


for nombre_tabla, datos_tabla in TABLAS_SILVER.items():
    guardar_tabla_silver(datos_tabla, nombre_tabla)

print("Transformación Silver finalizada")
