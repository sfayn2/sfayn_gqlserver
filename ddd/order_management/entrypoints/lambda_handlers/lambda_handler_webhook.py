import json
import logging
from ddd.order_management.application import message_bus, commands

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    """
    AWS Lambda Adapter for Webhook Entrypoints
    Handles routing based on the API Gateway Proxy Path
    """
    path = event.get("path", "")
    method = event.get("httpMethod", "POST")
    headers = event.get("headers", {})
    body = event.get("body", "") # raw string/bytes as expected by commands
    path_params = event.get("pathParameters") or {}

    logger.info(f"Processing webhook for path: {path}")

    if method != "POST":
        return _response({"success": False, "message": "Only POST is allowed"}, 400)

    try:
        # 1. Routing & Command Mapping
        if "add-order" in path:
            tenant_id = path_params.get("tenant_id") or path_params.get("proxy", "").split("/")[-1]
            command = commands.PublishAddOrderCommand.model_validate({
                "headers": headers,
                "raw_body": body,
                "request_path": path,
                "tenant_id": tenant_id
            })

        elif "shipment-tracker" in path:
            # Check if it's the Tenant version or SaaS version
            tenant_id = path_params.get("tenant_id")
            saas_id = path_params.get("saas_id")

            if tenant_id:
                command = commands.PublishShipmentTrackerTenantCommand.model_validate({
                    "headers": headers,
                    "raw_body": body,
                    "request_path": path,
                    "tenant_id": tenant_id
                })
            else:
                command = commands.PublishShipmentTrackerCommand.model_validate({
                    "headers": headers,
                    "raw_body": body,
                    "request_path": path,
                    "saas_id": saas_id or "default"
                })
        
        else:
            return _response({"success": False, "message": f"No handler for path {path}"}, 404)

        # 2. Execute via Message Bus
        result = message_bus.handle(command)
        return _response(result.model_dump())

    except Exception as e:
        logger.error(f"Error handling webhook: {str(e)}", exc_info=True)
        return _response({"success": False, "message": str(e)}, 500)

def _response(data, status=200):
    """Utility to format API Gateway compatible responses"""
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(data)
    }

