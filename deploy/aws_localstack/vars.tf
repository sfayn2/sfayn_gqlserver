variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "tenantoms"
}

variable "environment" {
  type    = string
  default = "prod"
}

variable "lambda_runtime" {
  type        = string
  description = "The Python runtime for all Lambda functions"
  default     = "python3.10"
}


