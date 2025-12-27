provider "aws" {
  region     = var.aws_region
  access_key = "test" # LocalStack ignores these but needs them present
  secret_key = "test"

  # --- LocalStack 2025 Compatibility Flags ---
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = false # Set to false so data.aws_caller_identity works locally
  s3_use_path_style           = true

  endpoints {
    # Storage & Identity
    s3             = "http://localhost:4566"
    s3control      = "http://localhost:4566"
    iam            = "http://localhost:4566"
    
    # Compute & Database
    lambda         = "http://localhost:4566"
    dynamodb       = "http://localhost:4566"

    # API & Events (REQUIRED for your new setup)
    apigateway     = "http://localhost:4566"
    events         = "http://localhost:4566" # EventBridge
    cloudwatch     = "http://localhost:4566"
    logs           = "http://localhost:4566" # CloudWatch Logs
    
    # Optional but recommended for common projects
    sts            = "http://localhost:4566"
    sns            = "http://localhost:4566"
    sqs            = "http://localhost:4566"
  }
}

# These data sources will now correctly return "000000000000" (LocalStack's ID) 
# and your var.aws_region because of the endpoint mappings above.
data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

