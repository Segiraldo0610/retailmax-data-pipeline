output "workspace_name" {
  description = "Configured Fabric workspace name."
  value       = var.workspace_name
}

output "lakehouse_name" {
  description = "Configured Fabric Lakehouse name."
  value       = var.lakehouse_name
}

output "workspace_id" {
  description = "Fabric workspace ID when resources are deployed by Terraform."
  value       = var.deploy_with_terraform ? fabric_workspace.retailmax[0].id : null
}

output "lakehouse_id" {
  description = "Fabric Lakehouse ID when resources are deployed by Terraform."
  value       = var.deploy_with_terraform ? fabric_lakehouse.medallion[0].id : null
}
