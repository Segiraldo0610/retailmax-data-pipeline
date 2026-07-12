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

### Revisión visual en DBeaver

Finalmente revisé la carga desde DBeaver para confirmar visualmente que el esquema `source` existe en la base `retail_db`, que las siete tablas fueron creadas correctamente y que los conteos coinciden con la carga realizada desde Python. Esta revisión no reemplaza las validaciones automatizadas, pero me sirve como evidencia visual del estado de la fuente y como apoyo para explicar el proceso durante la sustentación.

### Preparación del trabajo Bronze

Antes de iniciar la ejecución real en Fabric, dejé preparada la base de la capa Bronze dentro de `/pipelines/bronze`. La decisión fue trabajar la ingesta desde archivos Parquet generados localmente y cargados al Lakehouse en `Files/source_parquet/`, porque la fuente PostgreSQL está corriendo en mi equipo y el trial de Fabric puede limitar conexiones directas hacia una base local.

En esta preparación definí que las tablas Bronze conservarán los datos casi crudos y agregarán metadatos de auditoría como fecha de ingesta, tabla origen, archivo origen y modo de carga. Esta decisión me permite validar trazabilidad sin mezclar todavía reglas de limpieza, que quedarán para la capa Silver.

### Cierre del día

Al finalizar el Día 2 quedó completa la fuente transaccional simulada y validada:

- datos sintéticos generados en modo `dev`;
- carga exitosa en PostgreSQL dentro del esquema `source`;
- validaciones iniciales ejecutadas sobre conteos, relaciones y reglas básicas;
- revisión visual realizada en DBeaver;
- base de ingesta Bronze preparada para Fabric.

Con esto dejé listo el punto de partida para llevar los datos al Lakehouse y comenzar el trabajo por capas.

## Día 3 - Ingesta Bronze en Microsoft Fabric

### Carga de archivos fuente al Lakehouse

Para iniciar la capa Bronze cargué los archivos Parquet generados localmente al Lakehouse `lh_retailmax_medallion` en Microsoft Fabric. Organicé los archivos dentro de `Files/source_parquet/` para separar claramente los datos de entrada de las carpetas propias de Bronze, Silver y Gold.

Esta decisión mantiene la trazabilidad del origen: primero tengo una zona de archivos fuente y luego creo las tablas Bronze desde esos archivos. Así evito mezclar la carga inicial con las transformaciones posteriores.

### Notebook de ingesta Bronze

La ingesta Bronze la trabajé desde un notebook de Fabric. El objetivo de esta etapa fue leer cada archivo fuente, crear una tabla Bronze equivalente y agregar campos de auditoría que ayuden a rastrear el origen del dato.

Los campos de auditoría definidos para Bronze fueron:

- fecha y hora de ingesta;
- nombre de la tabla origen;
- ruta o archivo fuente;
- capa del pipeline.

Decidí no aplicar reglas fuertes de limpieza en Bronze porque esta capa debe conservar el dato lo más cercano posible al origen. Las reglas de negocio y calidad quedan para Silver.

### Ajuste por compatibilidad de fechas en Parquet

Durante la lectura de los archivos Parquet en Fabric identifiqué un error de Spark relacionado con el tipo `TIMESTAMP(NANOS,false)`. Esto ocurrió porque algunos campos de fecha se estaban escribiendo en Parquet con una precisión que Spark en Fabric no podía interpretar correctamente.

Para resolverlo ajusté la generación de archivos Parquet y dejé las fechas como texto en formato `YYYY-MM-DD` dentro de la zona fuente. Esta solución es coherente con el modelo Medallion porque Bronze puede recibir el dato en un formato simple y compatible, mientras que Silver se encarga de convertir formalmente esos campos a tipo `date`.

Con este ajuste evité modificar manualmente los archivos en Fabric y mantuve el proceso reproducible desde la generación local.

### Validación Bronze

Después de corregir la compatibilidad de fechas, ejecuté nuevamente la ingesta Bronze y validé que las tablas cargaran correctamente en el Lakehouse. La validación se enfocó en confirmar que las siete tablas origen estuvieran disponibles y que los conteos coincidieran con los datos generados en el ambiente local.

### Cierre del día

Al finalizar el Día 3 quedó completa la primera capa del Lakehouse:

- archivos fuente cargados en `Files/source_parquet/`;
- ingesta Bronze ejecutada desde Fabric;
- problema de fechas en Parquet identificado, corregido y documentado;
- tablas Bronze creadas y validadas;
- criterio definido para dejar las conversiones de tipos en Silver.

## Día 4 - Transformaciones Silver y modelo Gold

### Construcción de la capa Silver

Con Bronze disponible, avancé a la capa Silver. En esta etapa transformé los datos crudos en tablas más confiables para análisis. El trabajo principal fue aplicar limpieza, tipado, reglas de calidad y protección de datos sensibles.

Las decisiones más importantes de Silver fueron:

- convertir fechas desde texto a tipo `date`;
- limpiar espacios y normalizar textos;
- ajustar campos numéricos para cantidades, precios, descuentos y montos;
- marcar ventas canceladas o no válidas;
- identificar cantidades inválidas y descuentos extremos;
- marcar productos agotados o en riesgo de quiebre de inventario;
- proteger el correo de clientes mediante `email_hash` y no exponer el correo original en la capa analítica.

Esta capa es importante porque separa el dato recibido del dato confiable. Si aparece una anomalía, no la elimino sin explicación; la marco con una bandera para que pueda analizarse después.

### Validación de la capa Silver

Después de construir Silver ejecuté validaciones para revisar conteos, tipos de datos y reglas principales. La validación confirmó que las tablas Silver quedaron disponibles y que las reglas de calidad se podían revisar de forma explícita.

También confirmé que las fechas ya quedaran convertidas correctamente después del ajuste realizado en Bronze. Esto valida que la decisión de guardar fechas como texto en la zona fuente y convertirlas en Silver funcionó como se esperaba.

### Construcción de la capa Gold

Con Silver validada, construí la capa Gold como modelo analítico del proyecto. Esta capa está orientada a responder preguntas de negocio y no solo a almacenar datos limpios.

El modelo Gold incluye:

- `gold_dim_producto`, con información analítica de productos;
- `gold_dim_tienda`, con información de tiendas;
- `gold_dim_cliente`, con información de clientes protegida y segmentable;
- `gold_fact_ventas`, como tabla principal de hechos de ventas;
- `gold_kpi_ventas_diarias`, para seguimiento diario de ventas y devoluciones;
- `gold_kpi_inventario_diario`, para revisar inventario, agotados y riesgo de quiebre;
- `gold_kpi_clientes_rfm`, para segmentación de clientes por recencia, frecuencia y valor monetario.

Decidí separar dimensiones, hechos y KPIs porque facilita el consumo analítico y permite explicar mejor el modelo. Las dimensiones describen entidades, la tabla de hechos registra eventos de venta y las tablas KPI resumen métricas relevantes para el negocio.

### Validación de la capa Gold

Finalmente ejecuté la validación de Gold. Esta validación confirma que las tablas analíticas existen, tienen registros y contienen las métricas esperadas para el escenario Retail.

Con Gold funcionando, el proyecto ya cuenta con un flujo completo desde generación de datos hasta tablas analíticas. El siguiente paso es cerrar la orquestación, reforzar evidencias y dejar la documentación lista para entrega.

### Cierre del día

Al finalizar el Día 4 quedaron implementadas y validadas las capas Silver y Gold:

- Silver con limpieza, tipado, reglas de calidad y protección de datos sensibles;
- Gold con dimensiones, hechos y KPIs;
- validaciones ejecutadas sobre ambas capas;
- documentación técnica actualizada con las decisiones más importantes;
- base lista para trabajar orquestación, calidad formal y entrega final.

## Día 5 - Orquestación y control de ejecución

### Selección del orquestador

Para la orquestación decidí usar Microsoft Fabric Data Factory Pipelines. Esta decisión es coherente con la plataforma seleccionada porque los notebooks, el Lakehouse y las tablas Delta ya están dentro del mismo workspace de Fabric.

No elegí un orquestador externo para esta prueba porque habría agregado complejidad adicional sin aportar mucho al objetivo principal. En este caso me interesa demostrar que el flujo puede ejecutarse de forma ordenada, con dependencias claras y validaciones entre capas.

### Definición del DAG

Documenté la definición lógica del pipeline en `/orchestration/orquestacion_retailmax_fabric.yaml`. Este archivo describe las actividades, el orden de ejecución, las dependencias, los notebooks sugeridos y las salidas esperadas.

El orden definido es:

1. validar archivos fuente;
2. ejecutar ingesta Bronze;
3. validar Bronze;
4. ejecutar transformación Silver;
5. validar Silver;
6. ejecutar modelo Gold;
7. validar Gold.

La idea principal es que cada validación funcione como una compuerta. Si Bronze no valida, Silver no debe ejecutarse. Si Silver no valida, Gold no debe construirse. Esta regla evita propagar errores hacia las capas analíticas.

### Idempotencia y manejo de errores

Durante el desarrollo mantuve las escrituras en modo `overwrite`. Para esta prueba me parece una decisión adecuada porque permite repetir ejecuciones sin duplicar registros y facilita validar el resultado final.

También definí una política simple de reintentos: un reintento por actividad, dos minutos de espera y timeout de treinta minutos. No busqué una configuración demasiado compleja porque el objetivo es que el pipeline sea entendible y reproducible.

### Supuesto de Fabric Trial

Como estoy trabajando sobre una capacidad Trial, dejé versionada la definición del pipeline en el repositorio. Si el entorno permite exportar el pipeline desde Fabric, esa evidencia se puede anexar en `/docs`. Si no lo permite, la definición YAML y el README de orquestación dejan claro cómo se debe construir el flujo dentro de la interfaz.

### Documentación de arquitectura y datos

También preparé documentación técnica complementaria dentro de `/docs` para cubrir los puntos solicitados en el enunciado:

- `arquitectura.md`: explica la arquitectura end-to-end, los componentes usados y las decisiones principales.
- `catalogo_datos.md`: resume tablas, capas, campos clave, reglas de calidad y tratamiento de datos sensibles.
- `modelo_entidad_relacion.md`: documenta el modelo relacional fuente y el modelo analítico Gold mediante diagramas Mermaid.

Con estos documentos busco que la solución no dependa solo del código. La idea es que el evaluador pueda entender el diseño, las relaciones y el propósito de cada capa sin tener que preguntarme primero.

### Validación CI/CD básica

Agregué un workflow de GitHub Actions en `.github/workflows/validacion.yml`. La intención no es desplegar recursos ni ejecutar cargas reales desde CI, porque eso requeriría credenciales y configuración adicional. Para esta prueba decidí usarlo como una validación básica y segura.

El workflow revisa:

- sintaxis de los scripts Python;
- lectura correcta de archivos YAML;
- formato de Terraform;
- validación de la configuración Terraform.

Esta decisión me ayuda a detectar errores simples antes de integrar cambios y aporta un control de calidad adicional sin sobrecomplicar la solución.

### Preparación de evidencias

Preparé una guía de evidencias en `/docs/evidencias/README_EVIDENCIAS.md`. Allí organicé las validaciones de consola que ya puedo demostrar y las capturas que debo tomar para la entrega final.

Decidí separar las evidencias en una carpeta propia para no mezclar documentación conceptual con pruebas de ejecución. También definí nombres sugeridos para las capturas, de forma que sea fácil relacionarlas con la fuente, Bronze, Silver, Gold, orquestación, IaC y CI/CD.

### Ejecución visual de la orquestación

Materialicé la orquestación en Microsoft Fabric mediante el pipeline visual `pl_retailmax_medallion`. El pipeline quedó compuesto por tres actividades de notebook conectadas por ejecución correcta:

1. `01_bronze_ingesta_validacion`;
2. `02_silver_transformacion_validacion`;
3. `03_gold_modelo_validacion`.

La ejecución terminó correctamente en las tres actividades. Con esto dejé evidencia de que el flujo puede ejecutarse de forma ordenada desde Fabric, no solamente desde notebooks individuales.

### Cierre del día

Al finalizar este bloque quedó definida la orquestación lógica del pipeline:

- orquestador seleccionado: Microsoft Fabric Data Factory Pipelines;
- DAG documentado en YAML;
- dependencias definidas entre Bronze, Silver y Gold;
- validaciones usadas como compuertas de calidad;
- criterio de idempotencia documentado;
- supuesto de Fabric Trial registrado;
- documentación de arquitectura, catálogo y modelo entidad-relación agregada;
- validación CI/CD básica agregada con GitHub Actions;
- guía de evidencias preparada para el cierre de entrega;
- pipeline visual de Fabric ejecutado correctamente.
