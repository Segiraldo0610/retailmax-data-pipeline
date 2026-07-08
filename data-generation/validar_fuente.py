from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sqlalchemy import create_engine, text

from cargar_a_postgres import obtener_url_base_datos


@dataclass(frozen=True)
class ConsultaValidacion:
    nombre: str
    sql: str
    esperado: str


CONSULTAS_VALIDACION = [
    ConsultaValidacion(
        nombre="conteos_por_tabla",
        esperado="informativo",
        sql="""
        SELECT 'mstr_proveedores' AS table_name, COUNT(*) AS rows FROM source.mstr_proveedores
        UNION ALL SELECT 'mstr_articulos', COUNT(*) FROM source.mstr_articulos
        UNION ALL SELECT 'mstr_tiendas', COUNT(*) FROM source.mstr_tiendas
        UNION ALL SELECT 'crm_miembros', COUNT(*) FROM source.crm_miembros
        UNION ALL SELECT 'trans_ventas', COUNT(*) FROM source.trans_ventas
        UNION ALL SELECT 'inv_stock_diario', COUNT(*) FROM source.inv_stock_diario
        UNION ALL SELECT 'post_devoluciones', COUNT(*) FROM source.post_devoluciones
        ORDER BY table_name;
        """,
    ),
    ConsultaValidacion(
        nombre="ventas_sin_producto",
        esperado="0",
        sql="""
        SELECT COUNT(*) AS issue_count
        FROM source.trans_ventas v
        LEFT JOIN source.mstr_articulos p ON v.product_id = p.product_id
        WHERE p.product_id IS NULL;
        """,
    ),
    ConsultaValidacion(
        nombre="ventas_sin_tienda",
        esperado="0",
        sql="""
        SELECT COUNT(*) AS issue_count
        FROM source.trans_ventas v
        LEFT JOIN source.mstr_tiendas s ON v.store_id = s.store_id
        WHERE s.store_id IS NULL;
        """,
    ),
    ConsultaValidacion(
        nombre="devoluciones_sin_venta",
        esperado="0",
        sql="""
        SELECT COUNT(*) AS issue_count
        FROM source.post_devoluciones d
        LEFT JOIN source.trans_ventas v ON d.sale_id = v.sale_id
        WHERE v.sale_id IS NULL;
        """,
    ),
    ConsultaValidacion(
        nombre="ventas_cantidad_invalida",
        esperado="puede ser mayor a 0 por anomalias controladas",
        sql="SELECT COUNT(*) AS issue_count FROM source.trans_ventas WHERE quantity <= 0;",
    ),
    ConsultaValidacion(
        nombre="ventas_descuento_extremo",
        esperado="puede ser mayor a 0 por anomalias controladas",
        sql="SELECT COUNT(*) AS issue_count FROM source.trans_ventas WHERE discount_rate > 0.80;",
    ),
    ConsultaValidacion(
        nombre="stock_negativo",
        esperado="0",
        sql="SELECT COUNT(*) AS issue_count FROM source.inv_stock_diario WHERE stock_on_hand < 0;",
    ),
]


def ejecutar_validaciones() -> None:
    motor = create_engine(obtener_url_base_datos())

    with motor.connect() as conexion:
        for validacion in CONSULTAS_VALIDACION:
            print(f"\n== {validacion.nombre} ==")
            print(f"Esperado: {validacion.esperado}")
            resultado = pd.read_sql_query(text(validacion.sql), conexion)
            print(resultado.to_string(index=False))


if __name__ == "__main__":
    ejecutar_validaciones()
