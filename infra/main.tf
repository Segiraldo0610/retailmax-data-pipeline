locals {
  normalized_capacity_id = trimspace(var.fabric_capacity_id)
}

resource "fabric_workspace" "retailmax" {
  count = var.deploy_with_terraform ? 1 : 0

  display_name = var.workspace_name
  description  = "Workspace de desarrollo para el pipeline RetailMax."

  capacity_id                    = local.normalized_capacity_id != "" ? local.normalized_capacity_id : null
  skip_capacity_state_validation = var.skip_capacity_state_validation
}

resource "fabric_lakehouse" "medallion" {
  count = var.deploy_with_terraform ? 1 : 0

  display_name = var.lakehouse_name
  description  = "Lakehouse principal para las capas Bronze, Silver y Gold."
  workspace_id = fabric_workspace.retailmax[0].id

  configuration = {
    enable_schemas = var.enable_lakehouse_schemas
  }
}
