output "s3_bucket_name" {
  value = aws_s3_bucket.assets.id
}

output "s3_bucket_arn" {
  value = aws_s3_bucket.assets.arn
}

output "s3_bucket_domain" {
  value = "http://localhost:4566/${aws_s3_bucket.assets.id}"
}

output "lambda_function_graphql_handler" {
  value = aws_lambda_function.tenantoms_graphql_handler.function_name
}

output "lambda_layers" {
  value = aws_lambda_layer_version.tenantoms_shared_layer.layer_name
}

output "graphql_url" {
  value = "http://localhost:4566/restapis/${aws_api_gateway_rest_api.tenantoms_api.id}/${aws_api_gateway_stage.api_stage.stage_name}/_user_request_/graphql"
}

