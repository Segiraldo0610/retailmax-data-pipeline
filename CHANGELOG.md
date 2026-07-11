# Changelog

## 2026-07-11

- Construí la capa Silver en Fabric con limpieza, tipado y reglas de calidad sobre las tablas Bronze.
- Convertí campos de fecha a tipo `date` en Silver, manteniendo Bronze como capa de aterrizaje compatible.
- Agregué banderas de calidad para ventas inválidas, descuentos extremos, ventas canceladas, inventario agotado y riesgo de quiebre.
- Protegí el correo de clientes mediante `email_hash` para evitar exponer el dato personal en capas analíticas.
- Construí la capa Gold con dimensiones de producto, tienda y cliente.
- Construí la tabla de hechos `gold_fact_ventas` como base analítica de las ventas.
- Agregué KPIs de ventas diarias, inventario diario y segmentación RFM de clientes.
- Ejecuté validaciones sobre las capas Silver y Gold para confirmar existencia de tablas, conteos y métricas principales.
- Definí la orquestación lógica del pipeline con Microsoft Fabric Data Factory Pipelines.
- Agregué documentación de orquestación en `/orchestration/README_ORCHESTRATION.md`.
- Agregué la definición del DAG en `/orchestration/pipeline_retailmax_fabric.yaml`.
- Agregué documentación de arquitectura en `/docs/arquitectura.md`.
- Agregué catálogo de datos en `/docs/catalogo_datos.md`.
- Agregué modelo entidad-relación y modelo analítico en `/docs/modelo_entidad_relacion.md`.
- Agregué workflow CI/CD en `.github/workflows/validacion.yml` para validar Python, YAML y Terraform.
- Actualicé la documentación del proyecto para reflejar el avance real del pipeline Medallion.

## 2026-07-09

- Cargué los archivos Parquet fuente al Lakehouse de Fabric en `Files/source_parquet/`.
- Ejecuté la ingesta Bronze desde notebook en Microsoft Fabric.
- Agregué metadatos de auditoría a las tablas Bronze para conservar trazabilidad del origen.
- Identifiqué un problema de compatibilidad entre Spark en Fabric y fechas Parquet con tipo `TIMESTAMP(NANOS,false)`.
- Ajusté la generación de Parquet para escribir fechas como texto en formato `YYYY-MM-DD`.
- Validé que la ingesta Bronze leyera correctamente los archivos ajustados y creara las tablas esperadas.

## 2026-07-08

- Ajusté la estructura del repositorio con base en la estructura recomendada por el enunciado.
- Dejé el `README.md` principal en la raíz del proyecto y mantuve documentación ampliada dentro de `/docs`.
- Agregué el diario técnico como documento complementario en `/docs/DIARIO_TECNICO.md`.
- Incorporé el modelo inicial de datos fuente en `/docs/modelo_datos_source.md`.
- Preparé los scripts de generación, carga y validación de datos sintéticos en `/data-generation`.
- Cambié la convención de nombres del código propio a español para mantener coherencia con mi forma de trabajo.
- Renombré la configuración de generación a `config/generacion_datos.yaml`.
- Documenté en el README la función de los archivos de soporte del repositorio, como `.env.example`, `.gitignore`, `requirements.txt` y `docker-compose.yml`.
- Verifiqué que archivos sensibles o generados localmente, como `.env`, `.venv/`, `data/`, `.terraform/` y `tfstate`, no queden versionados.
- Generé datos sintéticos en modo `dev` para las siete tablas fuente del escenario RetailMax.
- Cargué los datos sintéticos en PostgreSQL dentro del esquema `source`.
- Ejecuté validaciones iniciales de conteos, relaciones y reglas básicas de calidad sobre la fuente.
- Complementé el README con las tecnologías y herramientas usadas en el proyecto, separando herramientas del pipeline y herramientas de apoyo.
- Revisé visualmente en DBeaver el esquema `source`, las tablas cargadas y los conteos principales.
- Preparé la base de la ingesta Bronze en Fabric, incluyendo documentación, notebook de carga y validación de conteos.

## 2026-07-07

- Inicié la planeación del proyecto.
- Seleccioné preliminarmente el escenario de Retail y comercio electrónico.
- Definí Microsoft Fabric como plataforma propuesta.
- Definí Terraform como estrategia principal para IaC, considerando el proveedor de Microsoft Fabric.
- Creé la estructura inicial del repositorio.

