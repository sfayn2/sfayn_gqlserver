output "s3_bucket_name" {
  value = aws_s3_bucket.assets.id
}

output "s3_bucket_arn" {
  value = aws_s3_bucket.assets.arn
}

output "s3_bucket_domain" {
  value = "http://localhost:4566/${aws_s3_bucket.assets.id}"
}

# LAMBDA OUTPUTS
output "lambda_function_graphql_handler" {
  value = aws_lambda_function.tenantoms_graphql_handler.function_name
}

output "lambda_function_webhook_receiver" {
  value = aws_lambda_function.tenantoms_webhook_receiver.function_name
}

output "lambda_function_event_worker" {
  value = aws_lambda_function.tenantoms_event_worker.function_name
}

output "lambda_layers" {
  value = aws_lambda_layer_version.tenantoms_shared_layer.layer_name
}

# API GATEWAY URLS (LocalStack Format)
output "api_base_invoke_url" {
  description = "The root URL of the API Stage (Dynamic)"
  value       = aws_api_gateway_stage.api_stage.invoke_url
}

output "graphql_url" {
  description = "Endpoint for GraphQL requests"
  # Concatenates the dynamic base URL with your specific path
  value       = "${aws_api_gateway_stage.api_stage.invoke_url}/graphql"
}

output "webhook_base_url" {
  description = "Base URL for webhooks. Append paths like /add-order/123 to this."
  value       = "${aws_api_gateway_stage.api_stage.invoke_url}/webhook"
}

# CONVENIENCE HELPER
output "example_webhook_order_url" {
  value = "${aws_api_gateway_stage.api_stage.invoke_url}/webhook/add-order/TENANT_ID"
}
