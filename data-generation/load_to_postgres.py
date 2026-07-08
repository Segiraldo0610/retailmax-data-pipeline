from __future__ import annotations

import argparse
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from generate_retail_data import PROJECT_ROOT, TABLE_FILES, TABLE_ORDER


DEFAULT_INPUT_DIR = PROJECT_ROOT / "data" / "source"


def get_database_url() -> str:
    load_dotenv(PROJECT_ROOT / ".env")

    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    database = os.getenv("POSTGRES_DB", "retail_db")
    user = os.getenv("POSTGRES_USER", "retail_user")
    password = os.getenv("POSTGRES_PASSWORD", "retail_pass")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"


def read_csv_table(input_dir: Path, logical_name: str) -> pd.DataFrame:
    table_name = TABLE_FILES[logical_name]
    path = input_dir / f"{table_name}.csv"
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    return pd.read_csv(path)


def load_tables(input_dir: Path, if_exists: str) -> dict[str, int]:
    engine = create_engine(get_database_url())
    row_counts: dict[str, int] = {}

    with engine.begin() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS source"))

        for logical_name in TABLE_ORDER:
            table_name = TABLE_FILES[logical_name]
            dataframe = read_csv_table(input_dir, logical_name)
            dataframe.to_sql(
                table_name,
                connection,
                schema="source",
                if_exists=if_exists,
                index=False,
                chunksize=5000,
                method="multi",
            )
            row_counts[table_name] = len(dataframe)

    return row_counts


def print_summary(row_counts: dict[str, int]) -> None:
    print("Carga finalizada en PostgreSQL, esquema source")
    print("")
    for table_name, row_count in row_counts.items():
        print(f"{table_name}: {row_count:,} filas")


def main() -> None:
    parser = argparse.ArgumentParser(description="Load generated RetailMax CSV files into PostgreSQL.")
    parser.add_argument("--input-dir", default=str(DEFAULT_INPUT_DIR), help="Directory with generated CSV files.")
    parser.add_argument("--if-exists", default="replace", choices=["fail", "replace", "append"], help="Load behavior.")
    args = parser.parse_args()

    row_counts = load_tables(Path(args.input_dir), args.if_exists)
    print_summary(row_counts)


if __name__ == "__main__":
    main()
