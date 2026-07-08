# Generacion de datos sinteticos

En esta carpeta estan los scripts para generar datos sinteticos del escenario RetailMax y cargarlos en PostgreSQL.

La generacion usa una semilla fija definida en `config/generation_config.yaml`, por lo que los resultados son reproducibles.

## Tablas generadas

- `source.mstr_proveedores`
- `source.mstr_articulos`
- `source.mstr_tiendas`
- `source.crm_miembros`
- `source.trans_ventas`
- `source.inv_stock_diario`
- `source.post_devoluciones`

## Perfiles de volumen

El archivo de configuracion tiene dos perfiles:

- `dev`: volumen reducido para pruebas rapidas durante el desarrollo.
- `full`: volumen objetivo definido para la prueba.

Para el desarrollo inicial uso `dev`, porque me permite validar estructura, relaciones y carga sin esperar demasiado tiempo.

## Ejecucion

Desde la raiz del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Generar datos en modo desarrollo:

```powershell
python data-generation/generate_retail_data.py --profile dev
```

Cargar datos en PostgreSQL:

```powershell
python data-generation/load_to_postgres.py
```

Validar conteos y reglas basicas:

```powershell
python data-generation/validate_source.py
```

## Salidas locales

Los archivos se generan en:

```text
data/source/
```

Esta carpeta no se versiona porque puede contener archivos grandes. El repositorio conserva el codigo y la configuracion para regenerarlos.

## Decisiones de diseno

- Uso PostgreSQL como fuente transaccional simulada.
- Cargo las tablas en el esquema `source`.
- Uso nombres fisicos en minuscula para facilitar consultas SQL en PostgreSQL.
- Mantengo algunos datos anomalos controlados para probar validaciones de calidad en las siguientes capas.

