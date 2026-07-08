# Changelog

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

## 2026-07-07

- Inicié la planeación del proyecto.
- Seleccioné preliminarmente el escenario de Retail y comercio electrónico.
- Definí Microsoft Fabric como plataforma propuesta.
- Definí Terraform como estrategia principal para IaC, considerando el proveedor de Microsoft Fabric.
- Creé la estructura inicial del repositorio.

