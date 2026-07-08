from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sqlalchemy import create_engine, text

from load_to_postgres import get_database_url


@dataclass(frozen=True)
class ValidationQuery:
    name: str
    sql: str
    expected: str


VALIDATION_QUERIES = [
    ValidationQuery(
        name="conteos_por_tabla",
        expected="informativo",
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
    ValidationQuery(
        name="ventas_sin_producto",
        expected="0",
        sql="""
        SELECT COUNT(*) AS issue_count
        FROM source.trans_ventas v
        LEFT JOIN source.mstr_articulos p ON v.product_id = p.product_id
        WHERE p.product_id IS NULL;
        """,
    ),
    ValidationQuery(
        name="ventas_sin_tienda",
        expected="0",
        sql="""
        SELECT COUNT(*) AS issue_count
        FROM source.trans_ventas v
        LEFT JOIN source.mstr_tiendas s ON v.store_id = s.store_id
        WHERE s.store_id IS NULL;
        """,
    ),
    ValidationQuery(
        name="devoluciones_sin_venta",
        expected="0",
        sql="""
        SELECT COUNT(*) AS issue_count
        FROM source.post_devoluciones d
        LEFT JOIN source.trans_ventas v ON d.sale_id = v.sale_id
        WHERE v.sale_id IS NULL;
        """,
    ),
    ValidationQuery(
        name="ventas_cantidad_invalida",
        expected="puede ser mayor a 0 por anomalias controladas",
        sql="SELECT COUNT(*) AS issue_count FROM source.trans_ventas WHERE quantity <= 0;",
    ),
    ValidationQuery(
        name="ventas_descuento_extremo",
        expected="puede ser mayor a 0 por anomalias controladas",
        sql="SELECT COUNT(*) AS issue_count FROM source.trans_ventas WHERE discount_rate > 0.80;",
    ),
    ValidationQuery(
        name="stock_negativo",
        expected="0",
        sql="SELECT COUNT(*) AS issue_count FROM source.inv_stock_diario WHERE stock_on_hand < 0;",
    ),
]


def run_validations() -> None:
    engine = create_engine(get_database_url())

    with engine.connect() as connection:
        for validation in VALIDATION_QUERIES:
            print(f"\n== {validation.name} ==")
            print(f"Esperado: {validation.expected}")
            dataframe = pd.read_sql_query(text(validation.sql), connection)
            print(dataframe.to_string(index=False))


if __name__ == "__main__":
    run_validations()
