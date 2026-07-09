# Este archivo está pensado para ejecutarse después de la ingesta Bronze
# en un notebook de Microsoft Fabric asociado al Lakehouse del proyecto.


CONTEOS_ESPERADOS_DEV = {
    "bronze_mstr_proveedores": 80,
    "bronze_mstr_articulos": 500,
    "bronze_mstr_tiendas": 30,
    "bronze_crm_miembros": 3000,
    "bronze_trans_ventas": 30000,
    "bronze_inv_stock_diario": 40000,
    "bronze_post_devoluciones": 1500,
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
    for nombre_tabla, total_esperado in CONTEOS_ESPERADOS_DEV.items():
        validar_conteo(nombre_tabla, total_esperado)

    print("Validación Bronze finalizada correctamente")


validar_tablas_bronze()
