from __future__ import annotations

import argparse
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from generar_datos_retail import ARCHIVOS_TABLAS, ORDEN_TABLAS, RAIZ_PROYECTO


CARPETA_ENTRADA_DEFAULT = RAIZ_PROYECTO / "data" / "source"

COLUMNAS_FECHA = {
    "mstr_articulos": ["launch_date"],
    "mstr_tiendas": ["opening_date"],
    "crm_miembros": ["birth_date", "registration_date"],
    "trans_ventas": ["sale_date"],
    "inv_stock_diario": ["snapshot_date"],
    "post_devoluciones": ["return_date"],
}


def obtener_url_base_datos() -> str:
    load_dotenv(RAIZ_PROYECTO / ".env")

    host = os.getenv("POSTGRES_HOST", "localhost")
    puerto = os.getenv("POSTGRES_PORT", "5432")
    base_datos = os.getenv("POSTGRES_DB", "retail_db")
    usuario = os.getenv("POSTGRES_USER", "retail_user")
    contrasena = os.getenv("POSTGRES_PASSWORD", "retail_pass")

    return f"postgresql+psycopg2://{usuario}:{contrasena}@{host}:{puerto}/{base_datos}"


def leer_csv_tabla(carpeta_entrada: Path, nombre_logico: str) -> pd.DataFrame:
    nombre_tabla = ARCHIVOS_TABLAS[nombre_logico]
    ruta_archivo = carpeta_entrada / f"{nombre_tabla}.csv"
    if not ruta_archivo.exists():
        raise FileNotFoundError(f"No encontre el archivo de entrada: {ruta_archivo}")

    columnas_fecha = COLUMNAS_FECHA.get(nombre_tabla, [])
    return pd.read_csv(ruta_archivo, parse_dates=columnas_fecha)


def cargar_tablas(carpeta_entrada: Path, si_existe: str) -> dict[str, int]:
    motor = create_engine(obtener_url_base_datos())
    conteos: dict[str, int] = {}

    with motor.begin() as conexion:
        conexion.execute(text("CREATE SCHEMA IF NOT EXISTS source"))

        for nombre_logico in ORDEN_TABLAS:
            nombre_tabla = ARCHIVOS_TABLAS[nombre_logico]
            datos_tabla = leer_csv_tabla(carpeta_entrada, nombre_logico)
            datos_tabla.to_sql(
                nombre_tabla,
                conexion,
                schema="source",
                if_exists=si_existe,
                index=False,
                chunksize=5000,
                method="multi",
            )
            conteos[nombre_tabla] = len(datos_tabla)

    return conteos


def imprimir_resumen_carga(conteos: dict[str, int]) -> None:
    print("Carga finalizada en PostgreSQL, esquema source")
    print("")
    for nombre_tabla, cantidad_filas in conteos.items():
        print(f"{nombre_tabla}: {cantidad_filas:,} filas")


def main() -> None:
    parser = argparse.ArgumentParser(description="Carga archivos CSV de RetailMax en PostgreSQL.")
    parser.add_argument("--carpeta-entrada", default=str(CARPETA_ENTRADA_DEFAULT), help="Carpeta con archivos CSV generados.")
    parser.add_argument(
        "--si-existe",
        default="reemplazar",
        choices=["fallar", "reemplazar", "agregar"],
        help="Comportamiento de carga si la tabla ya existe.",
    )
    argumentos = parser.parse_args()

    modo_carga = {
        "fallar": "fail",
        "reemplazar": "replace",
        "agregar": "append",
    }[argumentos.si_existe]
    conteos = cargar_tablas(Path(argumentos.carpeta_entrada), modo_carga)
    imprimir_resumen_carga(conteos)


if __name__ == "__main__":
    main()
