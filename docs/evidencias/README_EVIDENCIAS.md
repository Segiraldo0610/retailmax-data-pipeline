# Evidencias de ejecución

Este documento organiza las evidencias que acompañan la entrega del proyecto. La idea es que cada captura o salida técnica tenga un propósito claro y no se agreguen imágenes sin contexto.

## Evidencias de consola ya verificadas

Estas validaciones fueron ejecutadas localmente durante el cierre técnico:

| Evidencia | Comando | Resultado |
|---|---|---|
| Estado de Git | `git status --short` | Sin cambios versionables pendientes |
| Historial reciente | `git log --oneline -8` | Historial organizado y en español |
| Terraform válido | `terraform -chdir=infra validate` | `Success! The configuration is valid.` |
| Terraform formateado | `terraform -chdir=infra fmt -check` | Sin diferencias de formato |
| Sintaxis Python | `python -m compileall data-generation pipelines` | Compilación correcta |
| YAML válido | lectura de `config/generacion_datos.yaml`, `orchestration/orquestacion_retailmax_fabric.yaml` y `.github/workflows/validacion.yml` | Los tres archivos cargaron correctamente |

## Capturas recomendadas para la entrega

Las capturas deben tomarse limpias, sin pestañas personales visibles y sin mostrar credenciales. Sugiero guardarlas en `docs/evidencias/capturas/` con estos nombres:

| Archivo sugerido | Qué debe mostrar | Por qué sirve |
|---|---|---|
| `01_postgresql_dbeaver_source.png` | DBeaver con el esquema `source` y las siete tablas cargadas | Evidencia de fuente relacional simulada |
| `02_postgresql_conteos_source.png` | Consulta con conteos por tabla fuente | Confirma volumen cargado en PostgreSQL |
| `03_fabric_lakehouse_archivos_source_parquet.png` | Lakehouse con `Files/source_parquet/` y los siete Parquet | Evidencia de carga inicial en OneLake |
| `04_fabric_tablas_bronze.png` | Tablas `bronze_` visibles en el Lakehouse | Evidencia de ingesta Bronze |
| `05_fabric_validacion_bronze.png` | Salida del notebook de validación Bronze | Confirma conteos de Bronze |
| `06_fabric_validacion_silver.png` | Salida de validación Silver con métricas de calidad | Confirma limpieza, tipado y reglas |
| `07_fabric_validacion_gold.png` | Salida de validación Gold con resumen de KPIs | Confirma modelo analítico |
| `08_fabric_orquestacion_pipeline.png` | Pipeline o definición visual en Fabric, si se materializa | Evidencia de orquestación |
| `09_github_actions_validacion.png` | Ejecución exitosa del workflow en GitHub | Evidencia de CI/CD básico |

## Consultas de apoyo

Dejé dos consultas listas para tomar evidencias sin escribirlas desde cero:

- `docs/evidencias/consulta_conteos_source.sql`: conteos de las siete tablas del esquema `source` en PostgreSQL.
- `docs/evidencias/consulta_resumen_gold.sql`: resumen de ventas, devoluciones e inventario desde tablas Gold.

## Criterios para aceptar una captura

- Debe mostrar claramente el nombre del recurso o tabla.
- No debe mostrar contraseñas, tokens ni rutas personales innecesarias.
- Debe estar relacionada con un punto de la solución: fuente, Bronze, Silver, Gold, orquestación, IaC o CI/CD.
- Si una captura muestra un error corregido, solo se debe incluir si ayuda a explicar una decisión técnica. Para la entrega final priorizo capturas de ejecución correcta.

## Estado de evidencias

Al cierre de esta versión no dejo evidencias críticas pendientes. Si durante la revisión final se genera una nueva ejecución del pipeline o del workflow, puedo reemplazar las capturas por versiones más recientes.

## Evidencias capturadas

| Archivo | Estado | Observación |
|---|---|---|
| `docs/evidencias/capturas/01_postgresql_dbeaver_source.png` | Capturada | Muestra DBeaver conectado a `retail_db` con el esquema `source` y las siete tablas fuente. |
| `docs/evidencias/capturas/02_postgresql_conteos_source.png` | Capturada | Muestra DBeaver conectado a `retail_db`, el esquema `source`, las siete tablas y los conteos esperados. |
| `docs/evidencias/capturas/03_fabric_lakehouse_archivos_source_parquet.png` | Capturada | Muestra el Lakehouse `lh_retailmax_medallion` en `Files/source_parquet` con siete archivos Parquet cargados. |
| `docs/evidencias/capturas/04_fabric_tablas_bronze.png` | Capturada | Muestra las siete tablas `bronze_` creadas en el Lakehouse dentro de `Tables/dbo`. |
| `docs/evidencias/capturas/05_fabric_validacion_bronze.png` | Capturada | Muestra la validación de conteos Bronze ejecutada correctamente en Fabric. |
| `docs/evidencias/capturas/06a_fabric_validacion_silver_conteos_calidad.png` | Capturada | Muestra conteos correctos de Silver y primeras métricas de calidad. |
| `docs/evidencias/capturas/06b_fabric_validacion_silver_cierre.png` | Capturada | Muestra métricas finales de Silver y mensaje de validación correcta. |
| `docs/evidencias/capturas/07a_fabric_validacion_gold_conteos_kpis.png` | Capturada | Muestra conteos correctos de Gold y resumen de KPIs principales. |
| `docs/evidencias/capturas/07b_fabric_validacion_gold_cierre.png` | Capturada | Muestra KPIs de inventario y mensaje de validación Gold finalizada correctamente. |
| `docs/evidencias/capturas/08_fabric_orquestacion_pipeline.png` | Capturada | Muestra el pipeline visual `pl_retailmax_medallion` ejecutado correctamente con actividades Bronze, Silver y Gold. |
| `docs/evidencias/capturas/09_github_actions_validacion.png` | Capturada | Muestra el workflow de GitHub Actions finalizado correctamente sobre la rama `main`. |
