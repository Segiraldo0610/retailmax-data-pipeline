# Infraestructura como Codigo

En esta carpeta documento y versiono la estrategia de Infraestructura como Codigo del proyecto.

Para esta prueba elegi Terraform como herramienta principal de IaC porque me permite dejar la infraestructura expresada en archivos revisables, versionados y reutilizables. La plataforma seleccionada es Microsoft Fabric, por eso la configuracion usa el proveedor `microsoft/fabric`.

## Estado actual

El proyecto se esta desarrollando sobre una capacidad de prueba de Microsoft Fabric. Segun la documentacion del proveedor Terraform de Fabric, la capacidad Fabric Trial no esta soportada para el aprovisionamiento de capacidad desde el provider. Por esa razon, durante esta fase inicial cree el workspace y el Lakehouse desde la interfaz de Fabric y deje la definicion Terraform preparada con `deploy_with_terraform = false`.

Esta decision evita ejecutar un despliegue que podria fallar por una limitacion del trial, pero mantiene documentada la intencion de infraestructura y permite activar el despliegue si mas adelante cuento con una capacidad compatible.

## Recursos definidos

La configuracion Terraform representa estos recursos:

- Workspace de Microsoft Fabric: `ws_retailmax_data_dev`.
- Lakehouse principal: `lh_retailmax_medallion`.
- Soporte para esquemas en el Lakehouse.
- Variables separadas del codigo.
- Salidas basicas para identificar los recursos creados.

## Archivos principales

- `versions.tf`: define la version de Terraform y del proveedor `microsoft/fabric`.
- `provider.tf`: configura la autenticacion usando Azure CLI.
- `variables.tf`: centraliza los nombres y banderas de despliegue.
- `main.tf`: define el workspace y el Lakehouse de Fabric.
- `outputs.tf`: expone identificadores cuando el despliegue se ejecuta por Terraform.
- `terraform.tfvars.example`: muestra un ejemplo de parametros sin incluir secretos.

## Uso previsto

Primero valido la configuracion:

```powershell
terraform init
terraform validate
terraform plan
```

Mientras trabaje con Fabric Trial, mantengo:

```hcl
deploy_with_terraform = false
```

Si mas adelante uso una capacidad compatible de Fabric en Azure, puedo crear un archivo `terraform.tfvars` local, asignar el `fabric_capacity_id` y activar:

```hcl
deploy_with_terraform = true
```

## Supuesto documentado

Tomo como supuesto que el ambiente de prueba puede limitar algunas acciones de aprovisionamiento por codigo. Cuando eso ocurra, lo documento en el README y dejo evidencias de los recursos creados manualmente desde la interfaz de Fabric.

