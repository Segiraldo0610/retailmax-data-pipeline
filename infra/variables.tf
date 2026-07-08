variable "deploy_with_terraform" {
  description = "Controls whether Terraform should create Fabric resources. Default is false because Fabric Trial capacity has provider limitations."
  type        = bool
  default     = false
}

variable "workspace_name" {
  description = "Name of the Fabric workspace for the project."
  type        = string
  default     = "ws_retailmax_data_dev"
}

variable "lakehouse_name" {
  description = "Name of the main Fabric Lakehouse."
  type        = string
  default     = "lh_retailmax_medallion"
}

variable "fabric_capacity_id" {
  description = "Fabric capacity ID. Leave empty for the current trial-based setup."
  type        = string
  default     = ""
}

variable "enable_lakehouse_schemas" {
  description = "Enables schema support in the Lakehouse when the resource is deployed through Terraform."
  type        = bool
  default     = true
}

variable "skip_capacity_state_validation" {
  description = "Skips capacity validation when the caller cannot list capacities."
  type        = bool
  default     = false
}
