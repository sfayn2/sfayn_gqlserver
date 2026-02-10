import json
import base64
from typing import Dict, Any, Union, Optional
from ddd.order_management.application import message_bus, commands
from ddd.order_management.bootstrap import bootstrap_aws
bootstrap_aws.bootstrap_aws()



def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    High-Performance Webhook Receiver Adapter.
    Minimal logic to ensure sub-100ms response times.
    """
    # 1. Fast Extraction
    request_context = event.get("requestContext", {})
    path = request_context.get("path", event.get("path", ""))
    method = event.get("httpMethod", "").upper()
    
    # Normalize headers for signature verification logic (lowercase is standard)
    headers = {k.lower(): v for k, v in event.get("headers", {}).items()}

    # 2. Binary/Base64 Body Handling
    # Webhook providers (like Shopify/WSS) often send specific encodings
    body: Union[str, bytes] = event.get("body", "")
    if event.get("isBase64Encoded"):
        body = base64.b64decode(body)
    elif isinstance(body, str):
        body = body.encode("utf-8")

    # Traceability
    print(f"Webhook Received: {method} {path} [ReqID: {request_context.get('requestId')}]")

    if method != "POST":
        return _response({"success": False, "message": "Method Not Allowed"}, 405)

    try:
        command: Optional[commands.PublishAddOrderCommand | commands.PublishShipmentTrackerCommand] = None
        # 3. Routing Logic (Explicit & Strict)
        if "add-order" in path:
            tenant_id = path.rstrip("/").split("/")[-1]
            command = commands.PublishAddOrderCommand.model_validate({
                "headers": headers,
                "raw_body": body,
                "request_path": path,
                "tenant_id": tenant_id
            })

        elif "shipment-tracker" in path:
            # Check explicit params first, then positional path segments
            # it can be saas_id
            tenant_id = path.rstrip("/").split("/")[-1]

            command = commands.PublishShipmentTrackerCommand.model_validate({
                "headers": headers,
                "raw_body": body,
                "request_path": path,
                "tenant_id": tenant_id
            })
        
        else:
            msg = f"Unmatched webhook path: {path}"
            print(msg)
            return _response({"success": False, "message": msg }, 404)

        # 4. Dispatch to Domain
        # For webhooks, the message bus usually handles verification and queueing
        result = message_bus.handle(command)
        return _response(result.model_dump())

    except ValueError as e:
        # Pydantic validation failures (e.g., missing headers for signature)
        print(f"Webhook Validation Failed: {str(e)}")
        return _response({"success": False, "message": "Bad Request"}, 400)
    except Exception as e:
        print("Critical failure in webhook adapter:", e)
        return _response({"success": False, "message": "Internal Server Error"}, 500)

def _response(data: Dict[str, Any], status: int = 200) -> Dict[str, Any]:
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "X-Content-Type-Options": "nosniff"
        },
        "body": json.dumps(data)
    }
