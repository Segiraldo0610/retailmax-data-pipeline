# Generacion de datos sinteticos

En esta carpeta estan los scripts para generar datos sinteticos del escenario RetailMax y cargarlos en PostgreSQL.

La generacion usa una semilla fija definida en `config/generacion_datos.yaml`, por lo que los resultados son reproducibles.

## Convencion de nombres

En los scripts propios uso nombres en espanol para funciones, variables principales y argumentos de consola, porque es la forma en la que acostumbro escribir codigo y me facilita explicar la logica paso a paso.

Mantengo los nombres fisicos de tablas y columnas en ingles, por ejemplo `sale_id`, `product_id` y `net_amount`, porque los trato como el contrato tecnico de la fuente transaccional simulada. Esta convencion tambien facilita las consultas SQL y evita cambiar el modelo de datos cada vez que ajuste la logica interna de los scripts.

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
- `full`: volumen objetivo definido para la prueba y configurado como perfil por defecto.

El perfil `dev` queda como apoyo para pruebas rápidas. Para la entrega uso `full`, porque corresponde a los volúmenes mínimos del escenario Retail.

## Ejecucion

Desde la raiz del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Generar datos en modo entrega:

```powershell
python data-generation/generar_datos_retail.py
```

Generar datos en modo desarrollo, si necesito una prueba rápida:

```powershell
python data-generation/generar_datos_retail.py --perfil dev
```

Cargar datos en PostgreSQL:

```powershell
python data-generation/cargar_a_postgres.py
```

El script crea las tablas con la estructura inferida desde los CSV y luego usa `COPY` de PostgreSQL para cargar los datos de forma masiva. Tomé esta decisión porque el perfil `full` maneja tablas de alto volumen y una carga por lotes pequeños sería innecesariamente lenta.

Validar conteos y reglas basicas:

```powershell
python data-generation/validar_fuente.py
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
- Uso carga masiva con `COPY` para que el perfil `full` sea reproducible en tiempos razonables.
- Uso nombres fisicos en minuscula para facilitar consultas SQL en PostgreSQL.
- Mantengo algunos datos anomalos controlados para probar validaciones de calidad en las siguientes capas.
