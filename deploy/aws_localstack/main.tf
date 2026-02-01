# IAM

# 1. THE IAM ROLE
# ---------------------------------------------------------
resource "aws_iam_role" "tenantoms_lambda_role" {
  name = "${var.project_name}-${var.environment}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# 2. THE PERMISSIONS (Logging, EventBridge, and DynamoDB)
# ---------------------------------------------------------
resource "aws_iam_role_policy" "tenantoms_lambda_policy" {
  name = "${var.project_name}-${var.environment}-lambda-policy"
  role = aws_iam_role.tenantoms_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        # Allow Lambda to write logs to CloudWatch
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        Effect   = "Allow"
        Resource = "arn:aws:logs:${data.aws_region.current.region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${var.project_name}-*"
      },
      {
        # Allow First Handler to put events into EventBridge
        Action   = "events:PutEvents"
        Effect   = "Allow"
        Resource = "arn:aws:events:${data.aws_region.current.region}:${data.aws_caller_identity.current.account_id}:event-bus/default"
      },
      {
        # DynamoDB Read/Write Scoped to our Table
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:BatchWriteItem",
          "dynamodb:BatchGetItem"
        ]
        Effect   = "Allow"
        Resource = [
          aws_dynamodb_table.tenantoms_db.arn,
          "${aws_dynamodb_table.tenantoms_db.arn}/index/*" # Permission for the GSI
        ]
      },
    ]
  })
}


# IAM end



# 1. Primary S3 Bucket
resource "aws_s3_bucket" "assets" {
  bucket        = "${var.project_name}-${var.environment}-assets"
  force_destroy = true # Convenient for local testing
  
  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

# 2. Enable Versioning
resource "aws_s3_bucket_versioning" "assets_versioning" {
  bucket = aws_s3_bucket.assets.id
  versioning_configuration {
    status = "Enabled"
  }
}

# 3. Default Encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "assets_encryption" {
  bucket = aws_s3_bucket.assets.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}


# LAMBDA LAYER (Decoupled)
# ---------------------------------------------------------
# We define the S3 object but DO NOT provide a local "source".
# This tells Terraform: "Manage the metadata for this file in S3".
#resource "aws_s3_object" "tenantoms_layer_zip" {
#  bucket = aws_s3_bucket.assets.id
#  key    = "for_lambda/python_env.zip"
#  source = "${path.module}/python_env.zip"
#
#  # Trigger a re-upload if the local file changes
#  etag   = filemd5("${path.module}/python_env.zip")
#
#}

resource "aws_lambda_layer_version" "tenantoms_shared_layer" {
  layer_name          = "${var.project_name}-shared-dependencies"
  s3_bucket     = "hot-reload"
  s3_key        = var.lambda_function_s3_key_hot_reload_packages

  #s3_bucket           = aws_s3_bucket.assets.id
  #s3_key              = aws_s3_object.tenantoms_layer_zip.key
  #s3_object_version   = aws_s3_object.tenantoms_layer_zip.version_id
  compatible_runtimes = [var.lambda_runtime]

  # FORCED PROTECTION: Extra layer of safety
  #depends_on = [aws_s3_object.tenantoms_layer_zip]
}

#resource "aws_s3_object" "lambda_handler_zip" {
#  bucket = aws_s3_bucket.assets.id
#  key    = "for_lambda/source_ddd.zip"
#  source = "${path.module}/source_ddd.zip"
#
#  # Trigger a re-upload if the local file changes
#  etag   = filemd5("${path.module}/source_ddd.zip")
#
#}

# PRIMARY HANDLER (GraphQL)
# ---------------------------------------------------------

resource "aws_lambda_function" "tenantoms_graphql_handler" {
  function_name = "${var.project_name}-${var.environment}-graphql-api"
  role          = aws_iam_role.tenantoms_lambda_role.arn
  handler       = "ddd.order_management.entrypoints.lambda_handlers.lambda_handler_graphql.handler"
  runtime       = var.lambda_runtime # Reference variable here

  architectures = var.architectures
  s3_bucket     = "hot-reload"
  s3_key        = var.lambda_function_s3_key_hot_reload

  #s3_bucket         = aws_s3_bucket.assets.id
  #s3_key            = aws_s3_object.lambda_handler_zip.key
  #s3_object_version = aws_s3_object.lambda_handler_zip.version_id
  #layers            = [aws_lambda_layer_version.tenantoms_shared_layer.arn]

  # --- PRODUCTION PERFORMANCE TWEAKS slow JWKS fetches ---
  memory_size   = 256
  timeout       = 10
  # --------------------------------------




  #depends_on = [aws_s3_object.lambda_handler_zip]
  environment {
    variables = {
      DYNAMODB_TABLE_NAME  = aws_dynamodb_table.tenantoms_db.name
      PYTHONPATH = var.lambda_pythonpath
      ORDER_MANAGEMENT_INFRA_TYPE = "AWS"
      SKIP_JWT_VERIFY = "false"
    }
  }
}


# WEBHOOK RECEIVER LAMBDA HANDLER start here

# WEBHOOK RECEIVER HANDLER
# ---------------------------------------------------------

resource "aws_lambda_function" "tenantoms_webhook_receiver" {
  function_name = "${var.project_name}-${var.environment}-webhook-receiver"
  role          = aws_iam_role.tenantoms_lambda_role.arn
  handler       = "ddd.order_management.entrypoints.lambda_handlers.lambda_handler_webhook.handler"
  runtime       = var.lambda_runtime # Reference variable here
  architectures = var.architectures

  s3_bucket     = "hot-reload"
  s3_key        = var.lambda_function_s3_key_hot_reload

  #s3_bucket         = aws_s3_bucket.assets.id
  #s3_key            = aws_s3_object.lambda_handler_zip.key
  #s3_object_version = aws_s3_object.lambda_handler_zip.version_id
  #layers            = [aws_lambda_layer_version.tenantoms_shared_layer.arn]

  #depends_on = [aws_s3_object.lambda_handler_zip]


  
  environment {
    variables = {
      DYNAMODB_TABLE_NAME  = aws_dynamodb_table.tenantoms_db.name
      PYTHONPATH = var.lambda_pythonpath
      ORDER_MANAGEMENT_INFRA_TYPE = "AWS"
      SKIP_JWT_VERIFY = "false"
    }
  }
}


# WEBHOOK RECEIVER LAMBDA HANDLER end here

# ASYNC WORKER EVENTBRIDGE CONSUMER
# ---------------------------------------------------------

resource "aws_lambda_function" "tenantoms_event_worker" {
  function_name = "${var.project_name}-${var.environment}-event-worker"
  role          = aws_iam_role.tenantoms_lambda_role.arn
  handler       = "ddd.order_management.entrypoints.lambda_handlers.lambda_handler_eventbridge.handler"
  runtime       = var.lambda_runtime # Reference variable here

  s3_bucket     = "hot-reload"
  architectures = var.architectures
  s3_key        = var.lambda_function_s3_key_hot_reload

  #s3_bucket         = aws_s3_bucket.assets.id
  #s3_key            = aws_s3_object.lambda_handler_zip.key
  #s3_object_version = aws_s3_object.lambda_handler_zip.version_id
  #layers            = [aws_lambda_layer_version.tenantoms_shared_layer.arn]




  #depends_on = [aws_s3_object.lambda_handler_zip]
  environment {
    variables = {
      DYNAMODB_TABLE_NAME = aws_dynamodb_table.tenantoms_db.name
      PYTHONPATH = var.lambda_pythonpath
      ORDER_MANAGEMENT_INFRA_TYPE = "AWS"
      SKIP_JWT_VERIFY = "false"
    }
  }
}


# API GATEWAY start here

# 1. THE REST API CONTAINER
# ---------------------------------------------------------
resource "aws_api_gateway_rest_api" "tenantoms_api" {
  name        = "${var.project_name}-${var.environment}-api"
  description = "GraphQL/WebHook Receiver Gateway for TenantOMS"
  
  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

# 2. THE /graphql RESOURCE
# ---------------------------------------------------------
resource "aws_api_gateway_resource" "graphql_resource" {
  rest_api_id = aws_api_gateway_rest_api.tenantoms_api.id
  parent_id   = aws_api_gateway_rest_api.tenantoms_api.root_resource_id
  path_part   = "graphql"
}

# 3. THE POST METHOD (Standard for GraphQL)
# ---------------------------------------------------------
resource "aws_api_gateway_method" "graphql_post" {
  rest_api_id   = aws_api_gateway_rest_api.tenantoms_api.id
  resource_id   = aws_api_gateway_resource.graphql_resource.id
  http_method   = "POST"
  authorization = "NONE" # Use COGNITO or CUSTOMER for production
}

# 4. LAMBDA PROXY INTEGRATION
# ---------------------------------------------------------
# This sends the entire HTTP request to Lambda as a JSON event
resource "aws_api_gateway_integration" "graphql_lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.tenantoms_api.id
  resource_id             = aws_api_gateway_resource.graphql_resource.id
  http_method             = aws_api_gateway_method.graphql_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.tenantoms_graphql_handler.invoke_arn
}

# 5. PERMISSION FOR API GATEWAY TO CALL LAMBDA
# ---------------------------------------------------------
resource "aws_lambda_permission" "allow_api_gateway" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.tenantoms_graphql_handler.function_name
  principal     = "apigateway.amazonaws.com"

  # Scopes permission to this specific API Gateway
  source_arn = "${aws_api_gateway_rest_api.tenantoms_api.execution_arn}/*/*"
}

# 6. DEPLOYMENT & STAGE
# ---------------------------------------------------------
resource "aws_api_gateway_deployment" "api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.tenantoms_api.id

  # Triggers re-deployment if any integration/resource changes
  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.graphql_resource.id,
      aws_api_gateway_method.graphql_post.id,
      aws_api_gateway_integration.graphql_lambda_integration.id,
      aws_api_gateway_resource.webhook_proxy.id,
      aws_api_gateway_method.webhook_post.id,
      aws_api_gateway_integration.webhook_lambda_integration.id
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [aws_api_gateway_integration.graphql_lambda_integration]
}

resource "aws_api_gateway_stage" "api_stage" {
  deployment_id = aws_api_gateway_deployment.api_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.tenantoms_api.id
  stage_name    = var.environment
}


# API GATEWAY end here


# API GATEWAY FOR WEBHOOK HANDLER start here

# THE /webhook BASE RESOURCE
# ---------------------------------------------------------
resource "aws_api_gateway_resource" "webhook_resource" {
  rest_api_id = aws_api_gateway_rest_api.tenantoms_api.id
  parent_id   = aws_api_gateway_rest_api.tenantoms_api.root_resource_id
  path_part   = "webhook"
}

# THE GREEDY PROXY {proxy+}
# This captures any subpath: /webhook/add-order/123, /webhook/shipment-tracker, etc.
resource "aws_api_gateway_resource" "webhook_proxy" {
  rest_api_id = aws_api_gateway_rest_api.tenantoms_api.id
  parent_id   = aws_api_gateway_resource.webhook_resource.id
  path_part   = "{proxy+}"
}

# THE WEBHOOK POST METHOD
# ---------------------------------------------------------
resource "aws_api_gateway_method" "webhook_post" {
  rest_api_id   = aws_api_gateway_rest_api.tenantoms_api.id
  resource_id   = aws_api_gateway_resource.webhook_proxy.id
  http_method   = "POST"
  authorization = "NONE"
}

# WEBHOOK LAMBDA INTEGRATION
# ---------------------------------------------------------
resource "aws_api_gateway_integration" "webhook_lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.tenantoms_api.id
  resource_id             = aws_api_gateway_resource.webhook_proxy.id
  http_method             = aws_api_gateway_method.webhook_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.tenantoms_webhook_receiver.invoke_arn
}

# PERMISSION FOR API GATEWAY TO CALL WEBHOOK LAMBDA
# ---------------------------------------------------------
resource "aws_lambda_permission" "allow_api_gateway_webhook" {
  statement_id  = "AllowWebhookExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.tenantoms_webhook_receiver.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.tenantoms_api.execution_arn}/*/*"
}



# API GATEWAY FOR WEBHOOK HANDLER end here



# DYNAMODB Start here
# 1. SINGLE aABLE DYNAMODB DEFINITION
# ---------------------------------------------------------
resource "aws_dynamodb_table" "tenantoms_db" {
  name         = "${var.project_name}-${var.environment}-main-table"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk" # Partition Key (e.g. ORDER#ORD-1234)
  range_key    = "sk" # Sort Key (e.g. METADATA or ITEM#SKU-567)

  # Attributes must only be defined for keys used in PK/SK or Indexes
  attribute {
    name = "pk"
    type = "S"
  }

  attribute {
    name = "sk"
    type = "S"
  }

  # Global Secondary Index (GSI) for Tenant-based lookups
  # Useful for: "Get all orders for Tenant X"
  attribute {
    name = "tenant_id"
    type = "S"
  }

  global_secondary_index {
    name               = "TenantIndex"
    hash_key           = "tenant_id"
    range_key          = "pk"
    projection_type    = "ALL"
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}
# DYNAMODB End here



# EVENT BRIDGE Start Here
# 1. THE EVENTBRIDGE RULE
# ---------------------------------------------------------
# This rule watches the "default" bus for specific events
resource "aws_cloudwatch_event_rule" "order_events" {
  name        = "${var.project_name}-${var.environment}-order-rule"
  description = "Triggers worker when GraphQL handler puts an order event"

  # The JSON pattern that must match the event sent by your first Lambda
  event_pattern = jsonencode({
    "source": ["tenantoms.api"],
    "detail-type": ["OrderCreated", "OrderUpdated"]
  })
}

# 2. THE EVENTBRIDGE TARGET
# ---------------------------------------------------------
# This links the Rule to the Worker Lambda
resource "aws_cloudwatch_event_target" "worker_target" {
  rule      = aws_cloudwatch_event_rule.order_events.name
  target_id = "TenantOMSWorkerTarget"
  arn       = aws_lambda_function.tenantoms_event_worker.arn
}

# 3. LAMBDA PERMISSION FOR EVENTBRIDGE
# ---------------------------------------------------------
# Allows EventBridge to actually call (Invoke) your Worker Lambda
resource "aws_lambda_permission" "allow_eventbridge_to_worker" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.tenantoms_event_worker.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.order_events.arn
}

# EVENT BRIDGE End Here
