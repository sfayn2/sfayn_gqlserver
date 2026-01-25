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



variable "architectures" {
  type        = list(string)
  default     = ["arm64"]
}

