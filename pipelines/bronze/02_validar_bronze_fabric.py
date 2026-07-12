CONTEOS_ESPERADOS_FULL = {
    "bronze_mstr_proveedores": 800,
    "bronze_mstr_articulos": 5000,
    "bronze_mstr_tiendas": 150,
    "bronze_crm_miembros": 50000,
    "bronze_trans_ventas": 1000000,
    "bronze_inv_stock_diario": 750000,
    "bronze_post_devoluciones": 50000,
}


def contar_registros(nombre_tabla):
    return spark.table(nombre_tabla).count()


def validar_conteo(nombre_tabla, total_esperado):
    total_obtenido = contar_registros(nombre_tabla)

    if total_obtenido != total_esperado:
        raise ValueError(
            f"{nombre_tabla}: esperaba {total_esperado:,} registros "
            f"pero encontré {total_obtenido:,}"
        )

    print(f"{nombre_tabla}: conteo correcto ({total_obtenido:,})")


def validar_tablas_bronze():
    for nombre_tabla, total_esperado in CONTEOS_ESPERADOS_FULL.items():
        validar_conteo(nombre_tabla, total_esperado)

    print("Validación Bronze finalizada correctamente")


validar_tablas_bronze()
