import json
from ddd.order_management.bootstrap import bootstrap_aws
from ddd.order_management.entrypoints.graphql.schema import schema

def handler(event, context):

    try:
        # 3. Defensive Parsing
        raw_body = event.get("body")
        if not raw_body:
            return {"statusCode": 400, "body": json.dumps({"errors": [{"message": "Missing body"}]})}
            
        body = json.loads(raw_body)
        
        # 4. Execution
        result = schema.execute(
            body.get("query"),
            variable_values=body.get("variables", {}),
            context_value={"request_event": event} 
        )

        # 5. Robust Response Construction
        response_payload = {}
        if result.data is not None:
            response_payload["data"] = result.data
        
        if result.errors:
            # Log errors for internal debugging, but filter what goes to user
            response_payload["errors"] = [
                {"message": e.message if hasattr(e, 'message') else str(e)} 
                for e in result.errors
            ]

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(response_payload)
        }

    except json.JSONDecodeError:
        return {"statusCode": 400, "body": json.dumps({"errors": [{"message": "Invalid JSON"}]})}
    except Exception as e:
        # Log the real error to CloudWatch
        # Return generic error to user
        return {
            "statusCode": 500, 
            "body": json.dumps({"errors": [{"message": "Internal Server Error"}]})
        }



