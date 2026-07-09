# Diario Técnico

Este documento registra el proceso de trabajo, las decisiones técnicas, los supuestos y los aprendizajes obtenidos durante el desarrollo de la prueba. La idea es dejar trazabilidad del razonamiento seguido, no solo del resultado final.

El diario complementa el README del proyecto. Mientras el README explica la solución de forma consolidada, este documento muestra cómo fui avanzando, qué criterios usé para decidir y qué riesgos identifiqué durante el desarrollo.

## Día 1 - Planeación y preparación del ambiente

### Análisis inicial del enunciado

El primer paso fue revisar el enunciado oficial de la prueba técnica y la guía de cuentas cloud. A partir de esa revisión entendí que el reto no consiste únicamente en transformar datos, sino en construir una solución de ingeniería de datos de principio a fin.

Los componentes principales que identifiqué fueron:

- generación de datos sintéticos;
- carga en una base de datos relacional;
- arquitectura Medallion con capas Bronze, Silver y Gold;
- infraestructura como código;
- orquestación del pipeline;
- validaciones de calidad;
- gobierno y seguridad de datos;
- documentación técnica y evidencias de ejecución.

Con esto confirmé que antes de escribir código era necesario tomar decisiones de arquitectura, plataforma, herramientas y alcance.

También identifiqué una instrucción importante para la entrega: el README debe iniciar con el sector elegido, la plataforma cloud seleccionada y la justificación de ambas decisiones. Por esa razón decidí estructurar el README desde el inicio alrededor de esas dos decisiones principales.

Otro punto relevante del enunciado es que no existe una única solución correcta. La evaluación se enfoca en la coherencia técnica, la documentación de supuestos y la calidad del razonamiento. Esto refuerza la importancia de justificar cada decisión y no limitarme a entregar código sin explicación.

### Selección del escenario

Seleccioné el escenario B: Retail y comercio electrónico.

Tomé esta decisión porque es un escenario con reglas de negocio claras y medibles. Permite trabajar necesidades como ventas netas, inventario, alertas de quiebre de stock, devoluciones y segmentación RFM de clientes.

También consideré que es un escenario adecuado para el alcance de la prueba porque puedo construir una solución completa sin depender de conceptos regulatorios más complejos. Mi objetivo es que el proyecto sea sólido, entendible y defendible, sin aparentar una complejidad mayor a la necesaria.

### Selección de plataforma

La plataforma seleccionada inicialmente es Microsoft Fabric.

Elegí Fabric porque integra varias capacidades necesarias para el proyecto en un solo entorno: Lakehouse, notebooks de Spark, Data Factory Pipelines y componentes de análisis. Para una prueba de siete días, esta integración ayuda a reducir la complejidad operativa y permite concentrar el esfuerzo en el diseño del pipeline, la calidad de datos y la documentación.

También tuve en cuenta que Fabric aparece como una plataforma válida en el enunciado y que la guía de cuentas cloud menciona un trial gratuito de 60 días, lo cual reduce el riesgo de costos durante el desarrollo.

### Revisión del requisito de IaC

Uno de los puntos más importantes del enunciado es el requisito de Infraestructura como Código (IaC).

Entiendo IaC como la práctica de definir recursos de infraestructura mediante archivos versionados, en lugar de depender únicamente de pasos manuales en un portal. Esto permite que la configuración sea más reproducible, revisable y fácil de explicar.

Identifiqué un riesgo con Fabric: aunque es muy útil para construir el pipeline, algunas configuraciones del trial pueden realizarse desde la interfaz gráfica. Para reducir ese riesgo, decidí usar Terraform como estrategia principal de IaC, apoyándome en el proveedor de Microsoft Fabric cuando sea posible.

Si alguna configuración no se puede automatizar por limitaciones del trial, la documentaré como supuesto y dejaré evidencia clara de los pasos realizados.

### Arquitectura propuesta

La arquitectura seleccionada será Medallion, dividida en tres capas:

- Bronze: ingesta de datos crudos o casi crudos desde la fuente relacional.
- Silver: limpieza, tipado, validación, manejo de nulos, control de duplicados y protección de datos sensibles.
- Gold: modelo analítico, dimensiones, hechos, agregaciones, KPIs y reglas de negocio.

Elegí esta arquitectura porque separa responsabilidades y permite mantener trazabilidad desde el dato original hasta los indicadores finales.

### Fuente de datos

La fuente transaccional simulada será PostgreSQL ejecutado localmente con Docker.

Esta decisión me permite trabajar con una base relacional realista sin depender desde el inicio de una base cloud. Además, PostgreSQL es suficiente para simular las tablas origen del escenario y validar conteos, relaciones e integridad referencial antes de llevar los datos al Lakehouse.

### Preparación del ambiente local

Durante la preparación del ambiente local instalé y verifiqué las herramientas principales para el desarrollo:

- Git;
- Python;
- Visual Studio Code;
- Docker Desktop;
- DBeaver;
- Terraform;
- Azure CLI.

Estas herramientas son necesarias para versionar el proyecto, desarrollar los scripts, ejecutar PostgreSQL localmente, revisar la base de datos y preparar la estrategia de IaC.

Después de la instalación confirmé que las herramientas principales responden correctamente desde el entorno de Windows. Docker quedó instalado junto con Docker Compose, lo que permitió preparar la base relacional local del proyecto.

Durante la configuración de Docker fue necesario actualizar WSL y reiniciar Docker Desktop para que el motor pudiera iniciar correctamente. Después de eso validé la instalación ejecutando el contenedor de prueba `hello-world`.

Con Docker funcionando, levanté una instancia local de PostgreSQL usando Docker Compose. La base quedó disponible como `retail_db` y validé la conexión ejecutando una consulta de prueba dentro del contenedor. Esto deja preparada la fuente relacional que usaré más adelante para cargar los datos sintéticos.

También validé la conexión desde DBeaver, lo que me permitirá revisar las tablas de forma visual y generar evidencias de consultas cuando cargue los datos sintéticos.

### Supuestos iniciales

Hasta este momento tomé los siguientes supuestos:

- El proyecto se desarrollará sobre un solo escenario de negocio, como indica el enunciado.
- La solución debe priorizar claridad, reproducibilidad y buena documentación.
- Si una herramienta trial limita alguna configuración, esa limitación se documentará explícitamente.
- Si durante pruebas locales se reducen volúmenes, los scripts quedarán parametrizados para poder escalar a los volúmenes solicitados.
- La documentación se irá construyendo durante el desarrollo, no solo al final.

### Riesgos identificados

Los principales riesgos identificados al inicio fueron:

- elegir una plataforma cómoda para el pipeline pero débil para IaC;
- dedicar demasiado tiempo a configuración cloud y retrasar el desarrollo del pipeline;
- construir una solución sobredimensionada para el alcance de la prueba;
- dejar decisiones técnicas sin justificación suficiente.

Para manejar estos riesgos, decidí mantener una arquitectura sencilla, documentar supuestos y usar herramientas que pueda explicar con claridad en una entrevista técnica.

### Configuración inicial en Microsoft Fabric

Activé el acceso a Microsoft Fabric usando mi cuenta institucional y creé el workspace de desarrollo `ws_retailmax_data_dev` sobre la capacidad de prueba de Fabric. Dentro de ese workspace creé el Lakehouse principal `lh_retailmax_medallion`.

Esta configuración inicial deja preparado el espacio donde se organizarán las capas Bronze, Silver y Gold del pipeline.

También inicialicé el repositorio Git del proyecto y realicé el primer commit con la estructura base. Con esto dejé un punto de partida versionado para continuar el desarrollo de forma ordenada y poder evidenciar la evolución del trabajo.

Finalmente, cerré la decisión de continuar con Microsoft Fabric como plataforma principal. Revisé el riesgo asociado a IaC en Fabric Trial y decidí mitigarlo dejando la carpeta `/infra` preparada con Terraform, pero evitando ejecutar despliegues que puedan fallar por limitaciones de la capacidad de prueba. Si más adelante el trial bloquea algún requisito crítico, lo documentaré como supuesto y evaluaré una alternativa puntual, sin cambiar innecesariamente toda la arquitectura.

Validé la configuración inicial de Terraform ejecutando `terraform init`, `terraform validate` y `terraform plan`. La inicialización descargó correctamente el proveedor de Microsoft Fabric, la validación confirmó que la configuración es válida y el plan no mostró cambios sobre infraestructura real, únicamente las salidas configuradas para documentar los nombres del workspace y del Lakehouse.

### Cierre del día

Al finalizar el Día 1 quedaron listos los fundamentos del proyecto:

- escenario de negocio seleccionado: Retail y comercio electrónico;
- plataforma principal definida: Microsoft Fabric;
- estrategia de IaC definida y validada: Terraform;
- fuente relacional local preparada: PostgreSQL en Docker;
- arquitectura seleccionada: Medallion con capas Bronze, Silver y Gold;
- workspace y Lakehouse creados en Fabric;
- repositorio Git inicializado con commits de estructura e infraestructura;
- herramientas locales principales instaladas y verificadas.

Con esto considero cerrada la fase de preparación. El siguiente paso será iniciar la generación de datos sintéticos y cargarlos en PostgreSQL para comenzar el flujo real del pipeline.

## Día 2 - Generación de datos sintéticos y carga inicial

### Convención de nombres en el código

Al iniciar los scripts de generación y carga decidí mantener el código propio con nombres en español. Esta convención aplica principalmente para funciones, variables de control y argumentos de ejecución, porque es la forma en la que suelo escribir código y me ayuda a explicar la lógica con más naturalidad.

También decidí conservar los nombres físicos de columnas en inglés dentro de las tablas fuente, por ejemplo `sale_id`, `product_id`, `store_id` y `net_amount`. Lo hice porque esos campos funcionan como el contrato técnico de la fuente transaccional simulada. En un entorno real es común recibir sistemas origen con nombres en inglés, y para este proyecto me parece más importante documentarlos y transformarlos de forma consistente que traducirlos manualmente desde el inicio.

### Generación de datos sintéticos

Después de revisar la estructura de los scripts, validé que el proyecto ya contaba con datos sintéticos generados en modo `dev`. Este perfil lo uso para pruebas de desarrollo porque mantiene un volumen suficiente para validar relaciones y reglas sin hacer lenta cada ejecución.

Los archivos quedaron generados en la carpeta local `data/source/` en formato CSV y Parquet. Esta carpeta no se versiona porque contiene datos generados y puede crecer bastante cuando use el perfil completo.

Los conteos generados en modo `dev` fueron:

- `mstr_proveedores`: 80 registros.
- `mstr_articulos`: 500 registros.
- `mstr_tiendas`: 30 registros.
- `crm_miembros`: 3.000 registros.
- `trans_ventas`: 30.000 registros.
- `inv_stock_diario`: 40.000 registros.
- `post_devoluciones`: 1.500 registros.

### Carga en PostgreSQL

Con PostgreSQL activo en Docker y el contenedor `retailmax_postgres` en estado `healthy`, ejecuté el script de carga a PostgreSQL. El script tomó los CSV de `data/source/` y creó las tablas en el esquema `source` de la base `retail_db`.

La carga fue exitosa y mantuvo los mismos conteos del perfil `dev`. Para esta etapa decidí usar una carga con reemplazo de tablas, porque permite repetir el proceso durante el desarrollo sin duplicar registros. Esta decisión ayuda a mantener la idempotencia del flujo local.

### Validación inicial de la fuente

Después de la carga ejecuté el script de validación de fuente. Las validaciones revisan conteos, relaciones principales y algunos casos de calidad básicos, como ventas sin producto, ventas sin tienda, devoluciones sin venta, cantidades inválidas, descuentos extremos y stock negativo.

Las anomalías de cantidad inválida y descuento extremo pueden aparecer de forma controlada, porque las dejé intencionalmente en la generación para poder probar reglas de calidad en la capa Silver. En cambio, las validaciones de integridad relacional deben mantenerse en cero.

Con este paso dejé lista la fuente transaccional simulada para iniciar la ingesta hacia la capa Bronze.
