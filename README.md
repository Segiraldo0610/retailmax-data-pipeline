# Prueba Técnica DataKnow - Pipeline End-to-End de Ingeniería de Datos

**Postulante:** Samuel Enrique Giraldo Sabogal  
**Perfil:** Ingeniero / Científico de Datos Junior  
**Fecha de inicio:** 7 de julio de 2026  
**Modalidad:** Repositorio Git + evidencias de ejecución + documentación técnica

## Sector elegido, plataforma cloud y justificación

Para esta prueba seleccioné el **escenario B: Retail y comercio electrónico** y la plataforma cloud **Microsoft Fabric**.

Elegí el escenario de Retail porque plantea reglas de negocio claras y medibles: ventas netas, inventario, devoluciones, segmentación RFM de clientes y alertas de quiebre de stock. Considero que este escenario se ajusta bien al alcance de la prueba porque permite construir una solución completa de ingeniería de datos sin depender de conceptos regulatorios más complejos. Además, las necesidades del negocio se pueden traducir de forma directa en tablas analíticas, reglas de calidad y KPIs.

Elegí Microsoft Fabric porque es una de las plataformas válidas en el enunciado y porque integra en un mismo entorno varias capacidades necesarias para el proyecto: Lakehouse, notebooks de Spark, Data Factory Pipelines y componentes de análisis. Para una prueba de siete días, esta decisión me permite concentrarme en el diseño del pipeline, la calidad de datos y la documentación, reduciendo la complejidad de administrar muchos servicios separados.

Para cubrir el requisito de Infraestructura como Código, usaré **Terraform** como estrategia principal. En los recursos de Fabric que puedan administrarse por código, me apoyaré en el proveedor de Terraform para Microsoft Fabric. Si alguna configuración del trial requiere pasos desde la interfaz gráfica, documentaré el supuesto, el procedimiento y la evidencia correspondiente.

## Resumen ejecutivo

Este proyecto presenta una solución end-to-end de ingeniería de datos desarrollada para la prueba técnica de DataKnow. La solución parte de un escenario de negocio de Retail y comercio electrónico, genera datos sintéticos, los carga en una fuente relacional y los procesa mediante una arquitectura Medallion con capas Bronze, Silver y Gold.

El objetivo principal es construir una solución clara, reproducible y técnicamente sustentada, cubriendo generación de datos, infraestructura como código, ingesta, transformación, calidad, gobierno, seguridad, orquestación y documentación. La intención no es construir una arquitectura innecesariamente compleja, sino una solución que pueda ejecutar, explicar y defender con criterio técnico.

## Objetivo

Diseñar e implementar un pipeline de datos end-to-end que permita tomar información desde una fuente transaccional simulada, procesarla por capas de calidad creciente y dejarla lista para análisis de negocio.

Los objetivos principales son:

- generar datos sintéticos con comportamiento realista;
- cargar esos datos en una base de datos relacional;
- construir las capas Bronze, Silver y Gold;
- aplicar reglas de negocio del escenario Retail;
- implementar controles de calidad de datos;
- documentar decisiones, supuestos, arquitectura y linaje;
- preparar una solución defendible desde el punto de vista técnico.

## Alineación con el enunciado

El enunciado indica que la solución debe demostrar competencias end-to-end de ingeniería de datos. Por eso organicé el proyecto considerando estos puntos:

- diseño de una arquitectura de datos coherente con el escenario seleccionado;
- generación y carga de datos sintéticos en una fuente SQL;
- uso de Infraestructura como Código;
- construcción de un pipeline con arquitectura Medallion;
- orquestación de tareas y manejo de dependencias;
- aplicación de seguridad, roles, permisos y notificaciones;
- documentación de supuestos y decisiones técnicas;
- entrega mediante repositorio Git, evidencias de ejecución y README completo.

También tuve en cuenta la regla de desarrollar un único escenario de negocio y mantener consistencia en la plataforma cloud seleccionada durante toda la solución.

## Infraestructura como Código

Infraestructura como Código, o IaC, consiste en definir recursos cloud mediante archivos versionados en vez de crearlos únicamente desde el portal. Esto permite que la infraestructura sea más reproducible, revisable y fácil de documentar.

Para este proyecto usaré Terraform como estrategia principal de IaC. Esta decisión busca que la infraestructura no dependa únicamente de pasos manuales. En caso de que el trial de Fabric limite alguna automatización, documentaré la configuración realizada, la razón del supuesto y las evidencias necesarias.

En la fase inicial identifiqué una limitación relevante: la capacidad Fabric Trial puede restringir algunas acciones de aprovisionamiento mediante el proveedor de Terraform. Por eso dejé una estructura Terraform preparada en `/infra`, pero configurada por defecto para no desplegar recursos hasta contar con una capacidad compatible. Esta decisión evita forzar un despliegue inestable y mantiene la infraestructura documentada de forma reproducible.

## Supuestos iniciales

Durante el desarrollo voy a documentar los supuestos que tome para evitar ambigüedades. Hasta este momento considero los siguientes:

- seleccioné un solo escenario de negocio, como indica el enunciado;
- la solución debe ser clara, reproducible y defendible, sin sobreingeniería;
- si una herramienta gratuita o trial tiene limitaciones, las documentaré junto con la evidencia de lo implementado;
- si Fabric Trial no permite automatizar una configuración específica por Terraform, dejaré el recurso creado desde la interfaz, su justificación y el equivalente esperado en IaC;
- si reduzco volúmenes durante pruebas locales, dejaré la generación parametrizada para poder escalar a los volúmenes solicitados;
- la documentación se construirá durante todo el proyecto y no solo al final.

## Arquitectura propuesta

La arquitectura seguirá el patrón Medallion:

- Bronze: datos crudos o casi crudos, copiados desde la fuente con metadatos de auditoría.
- Silver: datos limpios, tipados, validados y con protección de datos sensibles.
- Gold: tablas analíticas, dimensiones, hechos, KPIs y agregaciones orientadas al negocio.

Esta separación permite mantener trazabilidad desde el dato original hasta los indicadores finales.

## Tecnologías y herramientas seleccionadas

Las tecnologías y herramientas usadas en el proyecto no cumplen todas el mismo rol. Algunas hacen parte directa del pipeline y otras las uso como apoyo para desarrollo, validación o documentación:

- Microsoft Fabric como plataforma principal de procesamiento, Lakehouse y orquestación.
- OneLake y Lakehouse de Fabric para organizar las capas Bronze, Silver y Gold.
- PostgreSQL como fuente relacional simulada para representar el sistema transaccional de RetailMax.
- Docker Desktop para ejecutar PostgreSQL localmente sin instalar la base directamente en Windows.
- Docker Compose para definir y levantar PostgreSQL como un servicio reproducible.
- Python para generación de datos, carga a PostgreSQL, validaciones y automatización local.
- Pandas y NumPy para construcción y manipulación de datos sintéticos.
- Faker para generar datos sintéticos con valores realistas.
- PyYAML para leer la configuración parametrizada de generación de datos.
- SQLAlchemy y psycopg2 para conectarme desde Python a PostgreSQL.
- python-dotenv para cargar variables locales desde `.env` sin exponer credenciales reales.
- PyArrow para escribir archivos Parquet durante la generación local.
- Terraform como estrategia principal de Infraestructura como Código.
- Azure CLI como herramienta de apoyo para autenticación y operación dentro del ecosistema Microsoft cuando sea necesario.
- DBeaver como cliente visual para revisar PostgreSQL y generar evidencias de consultas.
- Visual Studio Code como editor de código y documentación.
- PowerShell como consola principal de ejecución local.
- Git para control de versiones local y GitHub como plataforma prevista para la entrega del repositorio.
- GitHub Actions como validación CI/CD básica para revisar sintaxis, configuración y Terraform.
- Parquet y Delta Lake como formatos analíticos considerados para las capas del Lakehouse.

## Estructura inicial del repositorio

La estructura base del repositorio es:

```text
/.github
  /workflows
    validacion.yml
/infra
  README.md
/data-generation
  README_DATA_GENERATION.md
  generar_datos_retail.py
  cargar_a_postgres.py
  validar_fuente.py
/pipelines
  /bronze
  /silver
  /gold
/orchestration
  README_ORQUESTACION.md
  orquestacion_retailmax_fabric.yaml
/docs
  DIARIO_TECNICO.md
  arquitectura.md
  catalogo_datos.md
  /evidencias
    README_EVIDENCIAS.md
    /capturas
  modelo_datos_source.md
  modelo_entidad_relacion.md
/config
  generacion_datos.yaml
README.md
CHANGELOG.md
```

El `README.md` principal se mantiene en la raíz del repositorio porque el enunciado lo solicita como documento completo de la solución. La carpeta `docs/` contiene la documentación ampliada, incluyendo el diario técnico, la arquitectura, el catálogo de datos, el modelo de datos fuente, el modelo entidad-relación y las evidencias de ejecución. La carpeta `/infra` conserva su propio `README.md` porque allí deben quedar las instrucciones de despliegue de IaC.

## Archivos de soporte del repositorio

Además de las carpetas recomendadas por el enunciado, mantengo algunos archivos de soporte porque ayudan a que la solución sea reproducible y segura:

- `CHANGELOG.md`: lo conservo porque el enunciado lo solicita como historial de cambios con fecha y descripción.
- `.gitignore`: evita versionar archivos sensibles o generados localmente, como `.env`, `data/`, `.venv/`, `.terraform/` y archivos `tfstate`.
- `.env.example`: documenta las variables necesarias para ejecutar el proyecto sin exponer credenciales reales.
- `requirements.txt`: permite instalar las dependencias de Python de forma reproducible.
- `docker-compose.yml`: define la base PostgreSQL local usada como fuente transaccional simulada.
- `.github/workflows/validacion.yml`: define una validación CI/CD básica para revisar sintaxis de Python, archivos YAML y configuración Terraform antes de integrar cambios.
- `infra/.terraform.lock.hcl`: fija las versiones del proveedor de Terraform para que futuras ejecuciones usen la misma selección de dependencias. No contiene estado ni credenciales.

## Estado actual

El proyecto ya cuenta con una primera versión funcional del flujo Medallion: escenario de negocio definido, plataforma seleccionada, estructura del repositorio, configuración local de PostgreSQL, base Terraform en `/infra`, workspace de Fabric, Lakehouse principal y capas Bronze, Silver y Gold ejecutadas en Microsoft Fabric.

En Microsoft Fabric se creó el workspace `ws_retailmax_data_dev` y el Lakehouse `lh_retailmax_medallion`, que será utilizado para organizar las capas Bronze, Silver y Gold.

En el ambiente local generé datos sintéticos en modo `dev`, los cargué en PostgreSQL dentro del esquema `source` y ejecuté validaciones iniciales de conteos e integridad. Los conteos cargados y usados como base de comparación fueron:

| Tabla | Registros |
|---|---:|
| `source.mstr_proveedores` | 80 |
| `source.mstr_articulos` | 500 |
| `source.mstr_tiendas` | 30 |
| `source.crm_miembros` | 3.000 |
| `source.trans_ventas` | 30.000 |
| `source.inv_stock_diario` | 40.000 |
| `source.post_devoluciones` | 1.500 |

La configuración de Terraform fue inicializada, validada y planificada sin generar cambios sobre infraestructura real, debido a la protección definida para trabajar con Fabric Trial. Esta decisión mantiene documentada la estrategia de IaC sin forzar un despliegue inestable por limitaciones del trial.

La capa Bronze fue ejecutada en Fabric a partir de archivos Parquet cargados en el Lakehouse. Para evitar un problema de compatibilidad entre Parquet y Spark en Fabric con fechas almacenadas como `TIMESTAMP(NANOS,false)`, decidí escribir las fechas de los archivos fuente como texto en formato `YYYY-MM-DD`. Esta decisión mantiene Bronze como una capa de aterrizaje simple y compatible, y deja la conversión formal de tipos para Silver.

La capa Silver transforma las tablas Bronze en tablas limpias y tipadas. En esta etapa convertí fechas a tipo `date`, normalicé textos, ajusté campos numéricos, agregué banderas de calidad y protegí el correo de clientes usando un hash. Con esto evito exponer directamente un dato personal y dejo la información lista para análisis sin perder trazabilidad.

La capa Gold construye el modelo analítico principal del proyecto. Incluye dimensiones de producto, tienda y cliente, una tabla de hechos de ventas y tablas de KPIs para ventas diarias, inventario diario y segmentación RFM de clientes. Esta capa concentra las reglas de negocio que permiten responder preguntas del escenario Retail, como ventas netas, devoluciones, riesgo de quiebre de inventario y valor de clientes.

El estado resumido de las capas es:

| Componente | Estado | Resultado principal |
|---|---|---|
| Fuente PostgreSQL | Completado | Tablas `source` cargadas y validadas |
| Bronze | Completado | Tablas `bronze_` creadas desde archivos Parquet en Fabric |
| Silver | Completado | Datos limpios, tipados, validados y con reglas de calidad |
| Gold | Completado | Modelo analítico con dimensiones, hechos y KPIs |
| Orquestación | Definida | DAG lógico documentado para Microsoft Fabric Data Factory Pipelines |
| Documentación técnica | En avance | Arquitectura, catálogo de datos y modelo entidad-relación documentados |
| CI/CD | Definido | Workflow de GitHub Actions para validaciones básicas |
| Evidencias | En preparación | Guía de capturas y validaciones en `/docs/evidencias` |

Con este avance, el siguiente paso del proyecto es materializar o evidenciar la ejecución del pipeline en Fabric, completar evidencias, reforzar la documentación de calidad y preparar la entrega final del repositorio.
