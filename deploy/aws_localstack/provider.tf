provider "aws" {
  region                      = var.aws_region
  access_key                  = "test"
  secret_key                  = "test"
  
  # Necessary for LocalStack 2025 compatibility
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true

  endpoints {
    s3        = "http://localhost:4566"
    s3control = "http://localhost:4566"
    iam       = "http://localhost:4566"
    lambda    = "http://localhost:4566"
    dynamodb  = "http://localhost:4566"

  }
}


data "aws_region" "current" {}
data "aws_caller_identity" "current" {}


