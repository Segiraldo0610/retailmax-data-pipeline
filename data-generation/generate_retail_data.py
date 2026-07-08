from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from faker import Faker


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "generation_config.yaml"
OUTPUT_DIR = PROJECT_ROOT / "data" / "source"

TABLE_FILES = {
    "MSTR_PROVEEDORES": "mstr_proveedores",
    "MSTR_ARTICULOS": "mstr_articulos",
    "MSTR_TIENDAS": "mstr_tiendas",
    "CRM_MIEMBROS": "crm_miembros",
    "TRANS_VENTAS": "trans_ventas",
    "INV_STOCK_DIARIO": "inv_stock_diario",
    "POST_DEVOLUCIONES": "post_devoluciones",
}

TABLE_ORDER = list(TABLE_FILES)


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def resolve_row_counts(config: dict, profile: str) -> dict[str, int]:
    profiles = config.get("profiles", {})
    if profile not in profiles:
        valid_profiles = ", ".join(sorted(profiles))
        raise ValueError(f"Profile '{profile}' is not configured. Valid profiles: {valid_profiles}")

    selected_profile = profiles[profile]
    if selected_profile.get("use_target_rows"):
        return {
            table_name: int(table_config["target_rows"])
            for table_name, table_config in config["tables"].items()
        }

    return {table_name: int(selected_profile[table_name]) for table_name in TABLE_ORDER}


def random_dates(rng: np.random.Generator, start_date: str, end_date: str, size: int) -> pd.Series:
    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)
    days = (end - start).days
    offsets = rng.integers(0, days + 1, size=size)
    return start + pd.to_timedelta(offsets, unit="D")


def money(values: np.ndarray | pd.Series) -> np.ndarray:
    return np.round(values, 2)


def generate_suppliers(fake: Faker, rng: np.random.Generator, row_count: int) -> pd.DataFrame:
    countries = ["Colombia", "Mexico", "Peru", "Chile", "Estados Unidos", "Brasil"]
    categories = ["abarrotes", "tecnologia", "moda", "hogar", "belleza", "deportes"]

    records = []
    for idx in range(1, row_count + 1):
        records.append(
            {
                "supplier_id": f"SUP{idx:05d}",
                "supplier_name": fake.company(),
                "country": rng.choice(countries),
                "category_specialty": rng.choice(categories),
                "lead_time_days": int(rng.integers(2, 31)),
                "reliability_score": round(float(rng.uniform(0.70, 0.99)), 3),
                "is_active": bool(rng.choice([True, False], p=[0.94, 0.06])),
            }
        )

    return pd.DataFrame(records)


def generate_products(fake: Faker, rng: np.random.Generator, row_count: int, suppliers: pd.DataFrame) -> pd.DataFrame:
    catalog = {
        "abarrotes": ["bebidas", "snacks", "lacteos", "despensa"],
        "tecnologia": ["audio", "computo", "celulares", "accesorios"],
        "moda": ["camisetas", "calzado", "jeans", "chaquetas"],
        "hogar": ["cocina", "decoracion", "limpieza", "muebles"],
        "belleza": ["cuidado facial", "fragancias", "cabello", "maquillaje"],
        "deportes": ["fitness", "ciclismo", "running", "outdoor"],
    }
    brands = ["RetailMax", "Andes", "Nova", "Urban", "Natura", "Zenit", "Terra"]

    supplier_ids = suppliers["supplier_id"].to_numpy()
    records = []
    for idx in range(1, row_count + 1):
        category = str(rng.choice(list(catalog)))
        subcategory = str(rng.choice(catalog[category]))
        unit_cost = round(float(rng.uniform(4_000, 380_000)), 2)
        margin = float(rng.uniform(1.18, 1.75))
        launch_date = fake.date_between(start_date="-4y", end_date="today")

        records.append(
            {
                "product_id": f"PROD{idx:06d}",
                "sku": f"SKU-{idx:07d}",
                "product_name": f"{subcategory.title()} {fake.word().title()}",
                "category": category,
                "subcategory": subcategory,
                "brand": rng.choice(brands),
                "supplier_id": rng.choice(supplier_ids),
                "unit_cost": unit_cost,
                "unit_price": round(unit_cost * margin, 2),
                "launch_date": pd.Timestamp(launch_date),
                "is_active": bool(rng.choice([True, False], p=[0.96, 0.04])),
            }
        )

    return pd.DataFrame(records)


def generate_stores(rng: np.random.Generator, row_count: int) -> pd.DataFrame:
    city_region = [
        ("Bogota", "Centro"),
        ("Medellin", "Antioquia"),
        ("Cali", "Pacifico"),
        ("Barranquilla", "Caribe"),
        ("Bucaramanga", "Santander"),
        ("Pereira", "Eje Cafetero"),
        ("Cartagena", "Caribe"),
        ("Manizales", "Eje Cafetero"),
    ]
    formats = ["tienda_fisica", "ecommerce", "omnicanal"]

    records = []
    for idx in range(1, row_count + 1):
        city, region = city_region[int(rng.integers(0, len(city_region)))]
        store_format = str(rng.choice(formats, p=[0.62, 0.18, 0.20]))
        records.append(
            {
                "store_id": f"STORE{idx:04d}",
                "store_name": f"RetailMax {city} {idx:03d}",
                "city": city,
                "region": region,
                "store_format": store_format,
                "opening_date": pd.Timestamp("2018-01-01") + pd.to_timedelta(int(rng.integers(0, 2200)), unit="D"),
                "is_active": bool(rng.choice([True, False], p=[0.97, 0.03])),
            }
        )

    return pd.DataFrame(records)


def generate_members(fake: Faker, rng: np.random.Generator, row_count: int, start_date: str, end_date: str) -> pd.DataFrame:
    genders = ["F", "M", "NO_DECLARA"]
    segments = ["nuevo", "ocasional", "frecuente", "premium"]
    cities = ["Bogota", "Medellin", "Cali", "Barranquilla", "Bucaramanga", "Pereira", "Cartagena"]

    records = []
    for idx in range(1, row_count + 1):
        first_name = fake.first_name()
        last_name = fake.last_name()
        records.append(
            {
                "customer_id": f"CUST{idx:07d}",
                "member_code": f"RMX-{idx:08d}",
                "first_name": first_name,
                "last_name": last_name,
                "email": f"cliente{idx:07d}@retailmax.test",
                "gender": rng.choice(genders, p=[0.49, 0.48, 0.03]),
                "birth_date": pd.Timestamp(fake.date_of_birth(minimum_age=18, maximum_age=78)),
                "city": rng.choice(cities),
                "loyalty_segment": rng.choice(segments, p=[0.30, 0.34, 0.25, 0.11]),
                "registration_date": random_dates(rng, start_date, end_date, 1)[0],
            }
        )

    return pd.DataFrame(records)


def generate_sales(
    rng: np.random.Generator,
    row_count: int,
    products: pd.DataFrame,
    stores: pd.DataFrame,
    members: pd.DataFrame,
    start_date: str,
    end_date: str,
    include_anomalies: bool,
) -> pd.DataFrame:
    product_idx = rng.integers(0, len(products), size=row_count)
    store_idx = rng.integers(0, len(stores), size=row_count)
    customer_idx = rng.integers(0, len(members), size=row_count)

    product_ids = products["product_id"].to_numpy()[product_idx]
    store_ids = stores["store_id"].to_numpy()[store_idx]
    customer_ids = members["customer_id"].to_numpy()[customer_idx].astype(object)
    guest_mask = rng.random(row_count) < 0.035
    customer_ids[guest_mask] = None

    unit_prices = products["unit_price"].to_numpy()[product_idx]
    quantities = rng.choice([1, 2, 3, 4, 5], size=row_count, p=[0.46, 0.27, 0.15, 0.08, 0.04]).astype(int)
    discount_rates = rng.choice([0.00, 0.05, 0.10, 0.15, 0.20, 0.30], size=row_count, p=[0.45, 0.18, 0.16, 0.10, 0.07, 0.04])
    channels = rng.choice(["tienda", "web", "app", "marketplace"], size=row_count, p=[0.56, 0.22, 0.17, 0.05])
    statuses = rng.choice(["completada", "cancelada", "devuelta_parcial"], size=row_count, p=[0.93, 0.03, 0.04])

    if include_anomalies and row_count >= 500:
        anomaly_size = max(1, int(row_count * 0.002))
        anomaly_idx = rng.choice(row_count, size=anomaly_size, replace=False)
        quantities[anomaly_idx] = 0

        high_discount_idx = rng.choice(row_count, size=anomaly_size, replace=False)
        discount_rates[high_discount_idx] = 0.95

    gross_amount = quantities * unit_prices
    discount_amount = gross_amount * discount_rates
    net_amount = gross_amount - discount_amount

    return pd.DataFrame(
        {
            "sale_id": [f"SALE{idx:09d}" for idx in range(1, row_count + 1)],
            "sale_date": random_dates(rng, start_date, end_date, row_count),
            "store_id": store_ids,
            "customer_id": customer_ids,
            "product_id": product_ids,
            "channel": channels,
            "quantity": quantities,
            "unit_price": money(unit_prices),
            "discount_rate": discount_rates,
            "gross_amount": money(gross_amount),
            "discount_amount": money(discount_amount),
            "net_amount": money(net_amount),
            "payment_method": rng.choice(["tarjeta", "efectivo", "pse", "wallet"], size=row_count, p=[0.48, 0.18, 0.24, 0.10]),
            "order_status": statuses,
        }
    )


def generate_inventory(
    rng: np.random.Generator,
    row_count: int,
    products: pd.DataFrame,
    stores: pd.DataFrame,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    dates = pd.date_range(start_date, end_date, freq="D")
    total_combinations = len(dates) * len(stores) * len(products)
    replace = row_count > total_combinations
    combo_ids = rng.choice(total_combinations, size=row_count, replace=replace)

    product_index = combo_ids % len(products)
    store_index = (combo_ids // len(products)) % len(stores)
    date_index = combo_ids // (len(products) * len(stores))

    stock_on_hand = rng.integers(0, 220, size=row_count)
    reorder_point = rng.integers(12, 46, size=row_count)
    safety_stock = rng.integers(5, 20, size=row_count)

    stock_status = np.where(
        stock_on_hand == 0,
        "agotado",
        np.where(stock_on_hand <= reorder_point, "riesgo_quiebre", "disponible"),
    )

    return pd.DataFrame(
        {
            "inventory_id": [f"INV{idx:010d}" for idx in range(1, row_count + 1)],
            "snapshot_date": dates[date_index],
            "store_id": stores["store_id"].to_numpy()[store_index],
            "product_id": products["product_id"].to_numpy()[product_index],
            "stock_on_hand": stock_on_hand,
            "reorder_point": reorder_point,
            "safety_stock": safety_stock,
            "stock_status": stock_status,
        }
    )


def generate_returns(rng: np.random.Generator, row_count: int, sales: pd.DataFrame, end_date: str) -> pd.DataFrame:
    eligible_sales = sales[sales["quantity"] > 0].copy()
    sample_size = min(row_count, len(eligible_sales))
    selected = eligible_sales.sample(n=sample_size, random_state=int(rng.integers(0, 1_000_000))).reset_index(drop=True)

    return_days = rng.integers(1, 31, size=sample_size)
    return_dates = selected["sale_date"] + pd.to_timedelta(return_days, unit="D")
    max_return_date = pd.Timestamp(end_date) + pd.to_timedelta(30, unit="D")
    return_dates = return_dates.clip(upper=max_return_date)
    returned_quantity = np.minimum(selected["quantity"].to_numpy(), rng.choice([1, 2], size=sample_size, p=[0.86, 0.14]))
    refund_amount = returned_quantity * selected["unit_price"].to_numpy() * (1 - selected["discount_rate"].to_numpy())

    return pd.DataFrame(
        {
            "return_id": [f"RET{idx:08d}" for idx in range(1, sample_size + 1)],
            "sale_id": selected["sale_id"],
            "return_date": return_dates,
            "store_id": selected["store_id"],
            "customer_id": selected["customer_id"],
            "product_id": selected["product_id"],
            "returned_quantity": returned_quantity.astype(int),
            "return_reason": rng.choice(
                ["talla_color", "producto_defectuoso", "expectativa", "entrega_tardia", "otro"],
                size=sample_size,
                p=[0.24, 0.18, 0.31, 0.17, 0.10],
            ),
            "refund_amount": money(refund_amount),
            "return_channel": rng.choice(["tienda", "web", "app"], size=sample_size, p=[0.54, 0.28, 0.18]),
        }
    )


def write_outputs(tables: dict[str, pd.DataFrame], output_dir: Path, write_parquet: bool) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for logical_name, dataframe in tables.items():
        file_name = TABLE_FILES[logical_name]
        dataframe.to_csv(output_dir / f"{file_name}.csv", index=False, encoding="utf-8")
        if write_parquet:
            dataframe.to_parquet(output_dir / f"{file_name}.parquet", index=False)


def generate_tables(config: dict, profile: str) -> dict[str, pd.DataFrame]:
    seed = int(config["project"]["random_seed"])
    rng = np.random.default_rng(seed)
    fake = Faker("es_CO")
    Faker.seed(seed)

    row_counts = resolve_row_counts(config, profile)
    start_date = config["date_range"]["start_date"]
    end_date = config["date_range"]["end_date"]
    include_anomalies = bool(config.get("quality", {}).get("include_intentional_anomalies", False))

    suppliers = generate_suppliers(fake, rng, row_counts["MSTR_PROVEEDORES"])
    products = generate_products(fake, rng, row_counts["MSTR_ARTICULOS"], suppliers)
    stores = generate_stores(rng, row_counts["MSTR_TIENDAS"])
    members = generate_members(fake, rng, row_counts["CRM_MIEMBROS"], start_date, end_date)
    sales = generate_sales(
        rng,
        row_counts["TRANS_VENTAS"],
        products,
        stores,
        members,
        start_date,
        end_date,
        include_anomalies,
    )
    inventory = generate_inventory(rng, row_counts["INV_STOCK_DIARIO"], products, stores, start_date, end_date)
    returns = generate_returns(rng, row_counts["POST_DEVOLUCIONES"], sales, end_date)

    return {
        "MSTR_PROVEEDORES": suppliers,
        "MSTR_ARTICULOS": products,
        "MSTR_TIENDAS": stores,
        "CRM_MIEMBROS": members,
        "TRANS_VENTAS": sales,
        "INV_STOCK_DIARIO": inventory,
        "POST_DEVOLUCIONES": returns,
    }


def print_summary(tables: dict[str, pd.DataFrame], profile: str, output_dir: Path) -> None:
    print(f"Perfil utilizado: {profile}")
    print(f"Salida: {output_dir}")
    print("")
    for logical_name in TABLE_ORDER:
        print(f"{TABLE_FILES[logical_name]}: {len(tables[logical_name]):,} filas")


def main() -> None:
    config = load_config(CONFIG_PATH)
    default_profile = config["project"].get("default_profile", "dev")

    parser = argparse.ArgumentParser(description="Generate synthetic RetailMax source data.")
    parser.add_argument("--profile", default=default_profile, help="Configured profile to use: dev or full.")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR), help="Directory where CSV/Parquet files will be written.")
    parser.add_argument("--skip-parquet", action="store_true", help="Write only CSV files.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    tables = generate_tables(config, args.profile)
    write_outputs(tables, output_dir, write_parquet=not args.skip_parquet)
    print_summary(tables, args.profile, output_dir)


if __name__ == "__main__":
    main()
