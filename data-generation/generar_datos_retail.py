from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from faker import Faker


RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
RUTA_CONFIGURACION = RAIZ_PROYECTO / "config" / "generacion_datos.yaml"
CARPETA_SALIDA = RAIZ_PROYECTO / "data" / "source"

ARCHIVOS_TABLAS = {
    "MSTR_PROVEEDORES": "mstr_proveedores",
    "MSTR_ARTICULOS": "mstr_articulos",
    "MSTR_TIENDAS": "mstr_tiendas",
    "CRM_MIEMBROS": "crm_miembros",
    "TRANS_VENTAS": "trans_ventas",
    "INV_STOCK_DIARIO": "inv_stock_diario",
    "POST_DEVOLUCIONES": "post_devoluciones",
}

ORDEN_TABLAS = list(ARCHIVOS_TABLAS)


def leer_configuracion(ruta: Path) -> dict:
    with ruta.open("r", encoding="utf-8") as archivo:
        return yaml.safe_load(archivo)


def resolver_cantidad_filas(configuracion: dict, perfil: str) -> dict[str, int]:
    perfiles = configuracion.get("perfiles", {})
    if perfil not in perfiles:
        perfiles_validos = ", ".join(sorted(perfiles))
        raise ValueError(f"El perfil '{perfil}' no esta configurado. Perfiles validos: {perfiles_validos}")

    perfil_seleccionado = perfiles[perfil]
    if perfil_seleccionado.get("usar_filas_objetivo"):
        return {
            nombre_tabla: int(config_tabla["filas_objetivo"])
            for nombre_tabla, config_tabla in configuracion["tablas"].items()
        }

    return {nombre_tabla: int(perfil_seleccionado[nombre_tabla]) for nombre_tabla in ORDEN_TABLAS}


def generar_fechas_aleatorias(
    generador: np.random.Generator,
    fecha_inicio: str,
    fecha_fin: str,
    cantidad: int,
) -> pd.Series:
    inicio = pd.Timestamp(fecha_inicio)
    fin = pd.Timestamp(fecha_fin)
    dias = (fin - inicio).days
    desplazamientos = generador.integers(0, dias + 1, size=cantidad)
    return inicio + pd.to_timedelta(desplazamientos, unit="D")


def redondear_dinero(valores: np.ndarray | pd.Series) -> np.ndarray:
    return np.round(valores, 2)


def generar_proveedores(faker_es: Faker, generador: np.random.Generator, cantidad: int) -> pd.DataFrame:
    paises = ["Colombia", "Mexico", "Peru", "Chile", "Estados Unidos", "Brasil"]
    categorias = ["abarrotes", "tecnologia", "moda", "hogar", "belleza", "deportes"]

    registros = []
    for indice in range(1, cantidad + 1):
        registros.append(
            {
                "supplier_id": f"SUP{indice:05d}",
                "supplier_name": faker_es.company(),
                "country": generador.choice(paises),
                "category_specialty": generador.choice(categorias),
                "lead_time_days": int(generador.integers(2, 31)),
                "reliability_score": round(float(generador.uniform(0.70, 0.99)), 3),
                "is_active": bool(generador.choice([True, False], p=[0.94, 0.06])),
            }
        )

    return pd.DataFrame(registros)


def generar_productos(
    faker_es: Faker,
    generador: np.random.Generator,
    cantidad: int,
    proveedores: pd.DataFrame,
) -> pd.DataFrame:
    catalogo = {
        "abarrotes": ["bebidas", "snacks", "lacteos", "despensa"],
        "tecnologia": ["audio", "computo", "celulares", "accesorios"],
        "moda": ["camisetas", "calzado", "jeans", "chaquetas"],
        "hogar": ["cocina", "decoracion", "limpieza", "muebles"],
        "belleza": ["cuidado facial", "fragancias", "cabello", "maquillaje"],
        "deportes": ["fitness", "ciclismo", "running", "outdoor"],
    }
    marcas = ["RetailMax", "Andes", "Nova", "Urban", "Natura", "Zenit", "Terra"]

    ids_proveedor = proveedores["supplier_id"].to_numpy()
    registros = []
    for indice in range(1, cantidad + 1):
        categoria = str(generador.choice(list(catalogo)))
        subcategoria = str(generador.choice(catalogo[categoria]))
        costo_unitario = round(float(generador.uniform(4_000, 380_000)), 2)
        margen = float(generador.uniform(1.18, 1.75))
        fecha_lanzamiento = faker_es.date_between(start_date="-4y", end_date="today")

        registros.append(
            {
                "product_id": f"PROD{indice:06d}",
                "sku": f"SKU-{indice:07d}",
                "product_name": f"{subcategoria.title()} {faker_es.word().title()}",
                "category": categoria,
                "subcategory": subcategoria,
                "brand": generador.choice(marcas),
                "supplier_id": generador.choice(ids_proveedor),
                "unit_cost": costo_unitario,
                "unit_price": round(costo_unitario * margen, 2),
                "launch_date": pd.Timestamp(fecha_lanzamiento),
                "is_active": bool(generador.choice([True, False], p=[0.96, 0.04])),
            }
        )

    return pd.DataFrame(registros)


def generar_tiendas(generador: np.random.Generator, cantidad: int) -> pd.DataFrame:
    ciudades_regiones = [
        ("Bogota", "Centro"),
        ("Medellin", "Antioquia"),
        ("Cali", "Pacifico"),
        ("Barranquilla", "Caribe"),
        ("Bucaramanga", "Santander"),
        ("Pereira", "Eje Cafetero"),
        ("Cartagena", "Caribe"),
        ("Manizales", "Eje Cafetero"),
    ]
    formatos = ["tienda_fisica", "ecommerce", "omnicanal"]

    registros = []
    for indice in range(1, cantidad + 1):
        ciudad, region = ciudades_regiones[int(generador.integers(0, len(ciudades_regiones)))]
        formato_tienda = str(generador.choice(formatos, p=[0.62, 0.18, 0.20]))
        registros.append(
            {
                "store_id": f"STORE{indice:04d}",
                "store_name": f"RetailMax {ciudad} {indice:03d}",
                "city": ciudad,
                "region": region,
                "store_format": formato_tienda,
                "opening_date": pd.Timestamp("2018-01-01")
                + pd.to_timedelta(int(generador.integers(0, 2200)), unit="D"),
                "is_active": bool(generador.choice([True, False], p=[0.97, 0.03])),
            }
        )

    return pd.DataFrame(registros)


def generar_clientes(
    faker_es: Faker,
    generador: np.random.Generator,
    cantidad: int,
    fecha_inicio: str,
    fecha_fin: str,
) -> pd.DataFrame:
    generos = ["F", "M", "NO_DECLARA"]
    segmentos = ["nuevo", "ocasional", "frecuente", "premium"]
    ciudades = ["Bogota", "Medellin", "Cali", "Barranquilla", "Bucaramanga", "Pereira", "Cartagena"]

    registros = []
    for indice in range(1, cantidad + 1):
        nombre = faker_es.first_name()
        apellido = faker_es.last_name()
        registros.append(
            {
                "customer_id": f"CUST{indice:07d}",
                "member_code": f"RMX-{indice:08d}",
                "first_name": nombre,
                "last_name": apellido,
                "email": f"cliente{indice:07d}@retailmax.test",
                "gender": generador.choice(generos, p=[0.49, 0.48, 0.03]),
                "birth_date": pd.Timestamp(faker_es.date_of_birth(minimum_age=18, maximum_age=78)),
                "city": generador.choice(ciudades),
                "loyalty_segment": generador.choice(segmentos, p=[0.30, 0.34, 0.25, 0.11]),
                "registration_date": generar_fechas_aleatorias(generador, fecha_inicio, fecha_fin, 1)[0],
            }
        )

    return pd.DataFrame(registros)


def generar_ventas(
    generador: np.random.Generator,
    cantidad: int,
    productos: pd.DataFrame,
    tiendas: pd.DataFrame,
    clientes: pd.DataFrame,
    fecha_inicio: str,
    fecha_fin: str,
    incluir_anomalias: bool,
) -> pd.DataFrame:
    indice_producto = generador.integers(0, len(productos), size=cantidad)
    indice_tienda = generador.integers(0, len(tiendas), size=cantidad)
    indice_cliente = generador.integers(0, len(clientes), size=cantidad)

    ids_producto = productos["product_id"].to_numpy()[indice_producto]
    ids_tienda = tiendas["store_id"].to_numpy()[indice_tienda]
    ids_cliente = clientes["customer_id"].to_numpy()[indice_cliente].astype(object)
    mascara_invitados = generador.random(cantidad) < 0.035
    ids_cliente[mascara_invitados] = None

    precios_unitarios = productos["unit_price"].to_numpy()[indice_producto]
    cantidades = generador.choice([1, 2, 3, 4, 5], size=cantidad, p=[0.46, 0.27, 0.15, 0.08, 0.04]).astype(int)
    tasas_descuento = generador.choice(
        [0.00, 0.05, 0.10, 0.15, 0.20, 0.30],
        size=cantidad,
        p=[0.45, 0.18, 0.16, 0.10, 0.07, 0.04],
    )
    canales = generador.choice(["tienda", "web", "app", "marketplace"], size=cantidad, p=[0.56, 0.22, 0.17, 0.05])
    estados = generador.choice(["completada", "cancelada", "devuelta_parcial"], size=cantidad, p=[0.93, 0.03, 0.04])

    if incluir_anomalias and cantidad >= 500:
        cantidad_anomalias = max(1, int(cantidad * 0.002))
        indices_anomalias = generador.choice(cantidad, size=cantidad_anomalias, replace=False)
        cantidades[indices_anomalias] = 0

        indices_descuento_alto = generador.choice(cantidad, size=cantidad_anomalias, replace=False)
        tasas_descuento[indices_descuento_alto] = 0.95

    valor_bruto = cantidades * precios_unitarios
    valor_descuento = valor_bruto * tasas_descuento
    valor_neto = valor_bruto - valor_descuento

    return pd.DataFrame(
        {
            "sale_id": [f"SALE{indice:09d}" for indice in range(1, cantidad + 1)],
            "sale_date": generar_fechas_aleatorias(generador, fecha_inicio, fecha_fin, cantidad),
            "store_id": ids_tienda,
            "customer_id": ids_cliente,
            "product_id": ids_producto,
            "channel": canales,
            "quantity": cantidades,
            "unit_price": redondear_dinero(precios_unitarios),
            "discount_rate": tasas_descuento,
            "gross_amount": redondear_dinero(valor_bruto),
            "discount_amount": redondear_dinero(valor_descuento),
            "net_amount": redondear_dinero(valor_neto),
            "payment_method": generador.choice(["tarjeta", "efectivo", "pse", "wallet"], size=cantidad, p=[0.48, 0.18, 0.24, 0.10]),
            "order_status": estados,
        }
    )


def generar_inventario(
    generador: np.random.Generator,
    cantidad: int,
    productos: pd.DataFrame,
    tiendas: pd.DataFrame,
    fecha_inicio: str,
    fecha_fin: str,
) -> pd.DataFrame:
    fechas = pd.date_range(fecha_inicio, fecha_fin, freq="D")
    total_combinaciones = len(fechas) * len(tiendas) * len(productos)
    con_reemplazo = cantidad > total_combinaciones
    ids_combinacion = generador.choice(total_combinaciones, size=cantidad, replace=con_reemplazo)

    indice_producto = ids_combinacion % len(productos)
    indice_tienda = (ids_combinacion // len(productos)) % len(tiendas)
    indice_fecha = ids_combinacion // (len(productos) * len(tiendas))

    stock_disponible = generador.integers(0, 220, size=cantidad)
    punto_reorden = generador.integers(12, 46, size=cantidad)
    stock_seguridad = generador.integers(5, 20, size=cantidad)

    estado_stock = np.where(
        stock_disponible == 0,
        "agotado",
        np.where(stock_disponible <= punto_reorden, "riesgo_quiebre", "disponible"),
    )

    return pd.DataFrame(
        {
            "inventory_id": [f"INV{indice:010d}" for indice in range(1, cantidad + 1)],
            "snapshot_date": fechas[indice_fecha],
            "store_id": tiendas["store_id"].to_numpy()[indice_tienda],
            "product_id": productos["product_id"].to_numpy()[indice_producto],
            "stock_on_hand": stock_disponible,
            "reorder_point": punto_reorden,
            "safety_stock": stock_seguridad,
            "stock_status": estado_stock,
        }
    )


def generar_devoluciones(
    generador: np.random.Generator,
    cantidad: int,
    ventas: pd.DataFrame,
    fecha_fin: str,
) -> pd.DataFrame:
    ventas_elegibles = ventas[ventas["quantity"] > 0].copy()
    cantidad_muestra = min(cantidad, len(ventas_elegibles))
    seleccion = ventas_elegibles.sample(
        n=cantidad_muestra,
        random_state=int(generador.integers(0, 1_000_000)),
    ).reset_index(drop=True)

    dias_devolucion = generador.integers(1, 31, size=cantidad_muestra)
    fechas_devolucion = seleccion["sale_date"] + pd.to_timedelta(dias_devolucion, unit="D")
    fecha_devolucion_maxima = pd.Timestamp(fecha_fin) + pd.to_timedelta(30, unit="D")
    fechas_devolucion = fechas_devolucion.clip(upper=fecha_devolucion_maxima)
    cantidades_devueltas = np.minimum(
        seleccion["quantity"].to_numpy(),
        generador.choice([1, 2], size=cantidad_muestra, p=[0.86, 0.14]),
    )
    valor_devolucion = cantidades_devueltas * seleccion["unit_price"].to_numpy() * (1 - seleccion["discount_rate"].to_numpy())

    return pd.DataFrame(
        {
            "return_id": [f"RET{indice:08d}" for indice in range(1, cantidad_muestra + 1)],
            "sale_id": seleccion["sale_id"],
            "return_date": fechas_devolucion,
            "store_id": seleccion["store_id"],
            "customer_id": seleccion["customer_id"],
            "product_id": seleccion["product_id"],
            "returned_quantity": cantidades_devueltas.astype(int),
            "return_reason": generador.choice(
                ["talla_color", "producto_defectuoso", "expectativa", "entrega_tardia", "otro"],
                size=cantidad_muestra,
                p=[0.24, 0.18, 0.31, 0.17, 0.10],
            ),
            "refund_amount": redondear_dinero(valor_devolucion),
            "return_channel": generador.choice(["tienda", "web", "app"], size=cantidad_muestra, p=[0.54, 0.28, 0.18]),
        }
    )


def escribir_salidas(tablas: dict[str, pd.DataFrame], carpeta_salida: Path, escribir_parquet: bool) -> None:
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    for nombre_logico, datos_tabla in tablas.items():
        nombre_archivo = ARCHIVOS_TABLAS[nombre_logico]
        datos_tabla.to_csv(carpeta_salida / f"{nombre_archivo}.csv", index=False, encoding="utf-8")
        if escribir_parquet:
            datos_tabla.to_parquet(carpeta_salida / f"{nombre_archivo}.parquet", index=False)


def generar_tablas(configuracion: dict, perfil: str) -> dict[str, pd.DataFrame]:
    semilla = int(configuracion["proyecto"]["semilla_aleatoria"])
    generador = np.random.default_rng(semilla)
    faker_es = Faker("es_CO")
    Faker.seed(semilla)

    cantidad_filas = resolver_cantidad_filas(configuracion, perfil)
    fecha_inicio = configuracion["rango_fechas"]["fecha_inicio"]
    fecha_fin = configuracion["rango_fechas"]["fecha_fin"]
    incluir_anomalias = bool(configuracion.get("calidad", {}).get("incluir_anomalias_intencionales", False))

    proveedores = generar_proveedores(faker_es, generador, cantidad_filas["MSTR_PROVEEDORES"])
    productos = generar_productos(faker_es, generador, cantidad_filas["MSTR_ARTICULOS"], proveedores)
    tiendas = generar_tiendas(generador, cantidad_filas["MSTR_TIENDAS"])
    clientes = generar_clientes(faker_es, generador, cantidad_filas["CRM_MIEMBROS"], fecha_inicio, fecha_fin)
    ventas = generar_ventas(
        generador,
        cantidad_filas["TRANS_VENTAS"],
        productos,
        tiendas,
        clientes,
        fecha_inicio,
        fecha_fin,
        incluir_anomalias,
    )
    inventario = generar_inventario(generador, cantidad_filas["INV_STOCK_DIARIO"], productos, tiendas, fecha_inicio, fecha_fin)
    devoluciones = generar_devoluciones(generador, cantidad_filas["POST_DEVOLUCIONES"], ventas, fecha_fin)

    return {
        "MSTR_PROVEEDORES": proveedores,
        "MSTR_ARTICULOS": productos,
        "MSTR_TIENDAS": tiendas,
        "CRM_MIEMBROS": clientes,
        "TRANS_VENTAS": ventas,
        "INV_STOCK_DIARIO": inventario,
        "POST_DEVOLUCIONES": devoluciones,
    }


def imprimir_resumen(tablas: dict[str, pd.DataFrame], perfil: str, carpeta_salida: Path) -> None:
    print(f"Perfil utilizado: {perfil}")
    print(f"Salida: {carpeta_salida}")
    print("")
    for nombre_logico in ORDEN_TABLAS:
        print(f"{ARCHIVOS_TABLAS[nombre_logico]}: {len(tablas[nombre_logico]):,} filas")


def main() -> None:
    configuracion = leer_configuracion(RUTA_CONFIGURACION)
    perfil_default = configuracion["proyecto"].get("perfil_default", "dev")

    parser = argparse.ArgumentParser(description="Genera datos sinteticos para RetailMax.")
    parser.add_argument("--perfil", default=perfil_default, help="Perfil configurado: dev o full.")
    parser.add_argument("--carpeta-salida", default=str(CARPETA_SALIDA), help="Carpeta donde se escriben CSV y Parquet.")
    parser.add_argument("--solo-csv", action="store_true", help="Escribe solo archivos CSV.")
    argumentos = parser.parse_args()

    carpeta_salida = Path(argumentos.carpeta_salida)
    tablas = generar_tablas(configuracion, argumentos.perfil)
    escribir_salidas(tablas, carpeta_salida, escribir_parquet=not argumentos.solo_csv)
    imprimir_resumen(tablas, argumentos.perfil, carpeta_salida)


if __name__ == "__main__":
    main()
