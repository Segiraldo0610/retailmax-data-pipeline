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

## Tecnologías seleccionadas

Las tecnologías iniciales del proyecto son:

- Python para generación de datos, validaciones y automatización.
- Faker para datos sintéticos.
- PostgreSQL como fuente relacional simulada.
- Docker para ejecutar PostgreSQL localmente.
- Docker Compose para definir la base local como servicio reproducible.
- Microsoft Fabric como plataforma principal de procesamiento y orquestación.
- Terraform como estrategia principal de IaC.
- Parquet o Delta Lake como formato analítico.
- Git y GitHub para control de versiones y entrega.

## Estructura inicial del repositorio

La estructura base del repositorio es:

```text
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
/docs
  DIARIO_TECNICO.md
  modelo_datos_source.md
/config
  generacion_datos.yaml
README.md
CHANGELOG.md
```

El `README.md` principal se mantiene en la raíz del repositorio porque el enunciado lo solicita como documento completo de la solución. La carpeta `docs/` contiene la documentación ampliada, incluyendo el diario técnico, el modelo de datos fuente, el catálogo, los diagramas y las evidencias que se agreguen durante el desarrollo. La carpeta `/infra` conserva su propio `README.md` porque allí deben quedar las instrucciones de despliegue de IaC.

## Archivos de soporte del repositorio

Además de las carpetas recomendadas por el enunciado, mantengo algunos archivos de soporte porque ayudan a que la solución sea reproducible y segura:

- `CHANGELOG.md`: lo conservo porque el enunciado lo solicita como historial de cambios con fecha y descripción.
- `.gitignore`: evita versionar archivos sensibles o generados localmente, como `.env`, `data/`, `.venv/`, `.terraform/` y archivos `tfstate`.
- `.env.example`: documenta las variables necesarias para ejecutar el proyecto sin exponer credenciales reales.
- `requirements.txt`: permite instalar las dependencias de Python de forma reproducible.
- `docker-compose.yml`: define la base PostgreSQL local usada como fuente transaccional simulada.
- `infra/.terraform.lock.hcl`: fija las versiones del proveedor de Terraform para que futuras ejecuciones usen la misma selección de dependencias. No contiene estado ni credenciales.

## Estado actual

El proyecto se encuentra en fase inicial de implementación. Ya están definidos el escenario de negocio, la plataforma principal, la estrategia de IaC y la estructura base del repositorio. También quedó configurada una base PostgreSQL local en Docker para simular la fuente transaccional inicial.

En Microsoft Fabric se creó el workspace `ws_retailmax_data_dev` y el Lakehouse principal `lh_retailmax_medallion`, que será utilizado para organizar las capas Bronze, Silver y Gold.

Adicionalmente, el repositorio Git ya cuenta con una primera versión de la estructura del proyecto y una base Terraform en `/infra`. La configuración de Terraform fue inicializada, validada y planificada sin generar cambios sobre infraestructura real, debido a la protección definida para trabajar con Fabric Trial.
