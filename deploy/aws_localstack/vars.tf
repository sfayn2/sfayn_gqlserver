variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "tntoms"
}

variable "environment" {
  type    = string
  default = "tst"
}

variable "lambda_runtime" {
  type        = string
  description = "The Python runtime for all Lambda functions"
  default     = "python3.14"
}

variable "lambda_pythonpath" {
  type        = string
  default     = "/var/task/.venv/lib/python3.14/site-packages"
}

variable "lambda_function_s3_key_hot_reload" {
  type        = string
  description = "the absolute path to your source code for localstack hot-reloading"
}

variable "lambda_function_s3_key_hot_reload_packages" {
  type        = string
  description = "the absolute path to your packages for localstack hot-reloading"
}

variable "skip_jwt_verify" {
  type        = string
  description = "whether to skip JWT verification in localstack mode"
  default     = "false"
}


variable "architectures" {
  type        = list(string)
  description = "The CPU architecture for all Lambda functions"
  #default     = ["arm64"]
}

#x86_64



variable "internal_event_bus_name" {
  description = "The name of the internal EventBridge event bus"
  type        = string
  default     = "internal-bus"
}

variable "external_event_bus_name" {
  description = "The name of the external EventBridge event bus"
  type        = string
  default     = "external-bus"
}

variable "internal_event_source_name" {
  description = "The internal source name for EventBridge events"
  type        = list(string)
  default     = ["tenantoms.api"]
}

variable "external_event_source_name" {
  description = "The external source name for EventBridge events"
  type        = list(string)
  default     = ["tenantoms.api"]
}

variable "internal_order_detail_types" {
  description = "List of event detail-types to listen for internal event bus"
  type        = list(string)
  default     = ["shipping_tracker_webhook.received", "OrderUpdated"]
}

variable "external_order_detail_types" {
  description = "List of event detail-types to listen for external event bus"
  type        = list(string)
  default     = ["shipping_tracker_webhook.received", "OrderUpdated"]
}

