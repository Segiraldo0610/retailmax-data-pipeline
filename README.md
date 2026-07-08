# Prueba Técnica DataKnow - Pipeline End-to-End de Ingeniería de Datos

**Postulante:** Samuel Enrique Giraldo Sabogal  
**Perfil:** Ingeniero / Científico de Datos Junior  
**Fecha de inicio:** 7 de julio de 2026  
**Modalidad:** Repositorio Git + evidencias de ejecución + documentación técnica

## Resumen ejecutivo

Este proyecto presenta una solución end-to-end de ingeniería de datos desarrollada para la prueba técnica de DataKnow. La solución parte de un escenario de negocio de Retail y comercio electrónico, genera datos sintéticos, los carga en una fuente relacional y los procesa mediante una arquitectura Medallion con capas Bronze, Silver y Gold.

El objetivo principal es construir una solución clara, reproducible y técnicamente sustentada, cubriendo generación de datos, infraestructura como código, ingesta, transformación, calidad, gobierno, seguridad, orquestación y documentación.

## Sector elegido, plataforma cloud y justificación

Para esta prueba seleccioné el **escenario B: Retail y comercio electrónico** y la plataforma cloud **Microsoft Fabric**.

Elegí el escenario de Retail porque plantea reglas de negocio claras y medibles: ventas netas, inventario, devoluciones, segmentación RFM de clientes y alertas de quiebre de stock. Considero que este escenario se ajusta bien al alcance de la prueba porque permite construir una solución completa de ingeniería de datos sin depender de conceptos regulatorios más complejos. Además, las necesidades del negocio se pueden traducir de forma directa en tablas analíticas, reglas de calidad y KPIs.

Elegí Microsoft Fabric porque es una de las plataformas válidas en el enunciado y porque integra en un mismo entorno varias capacidades necesarias para el proyecto: Lakehouse, notebooks de Spark, Data Factory Pipelines y componentes de análisis. Para una prueba de siete días, esta decisión me permite concentrarme en el diseño del pipeline, la calidad de datos y la documentación, reduciendo la complejidad de administrar muchos servicios separados.

Para cubrir el requisito de Infraestructura como Código, usaré **Terraform** como estrategia principal. En los recursos de Fabric que puedan administrarse por código, me apoyaré en el proveedor de Terraform para Microsoft Fabric. Si alguna configuración del trial requiere pasos desde la interfaz gráfica, documentaré el supuesto, el procedimiento y la evidencia correspondiente.

## Introducción

Este proyecto desarrolla una solución end-to-end de ingeniería de datos para un escenario de negocio de Retail. La solución cubre el ciclo completo de trabajo: generación de datos sintéticos, carga en una fuente relacional, ingesta hacia una arquitectura Medallion, limpieza, transformación, construcción de tablas analíticas, validaciones de calidad, orquestación, gobierno, seguridad y documentación.

La intención no es construir una arquitectura innecesariamente compleja, sino una solución clara, reproducible y bien sustentada. Cada decisión técnica debe tener una razón concreta y debe poder explicarse durante una entrevista técnica.

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

La estructura propuesta para el repositorio es:

```text
/infra
/data-generation
/pipelines
  /bronze
  /silver
  /gold
/orchestration
/docs
/config
README.md
CHANGELOG.md
```

Esta estructura sigue la recomendación del enunciado y separa las responsabilidades principales del proyecto.

## Estado actual

El proyecto se encuentra en fase de preparación del ambiente y definición inicial de arquitectura. Ya están definidos el escenario de negocio, la plataforma principal, la estrategia de IaC y la estructura base del repositorio. También quedó configurada una base PostgreSQL local en Docker para simular la fuente transaccional inicial.

En Microsoft Fabric se creó el workspace `ws_retailmax_data_dev` y el Lakehouse principal `lh_retailmax_medallion`, que será utilizado para organizar las capas Bronze, Silver y Gold.
