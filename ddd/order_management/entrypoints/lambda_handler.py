import json
from ddd.order_management.infrastructure.bootstrap import bootstrap_aws
from ddd.order_management.entrypoints.graphql.schema import schema

def handler(event, context):
    try:

        body = json.loads(event.get("body", "{}"))
        
        # Execute with context_value so info.context is populated
        result = schema.execute(
            body.get("query"),
            variable_values=body.get("variables", {}),
            # Pass the event as context so resolvers can see headers/cookies
            context_value={"request_event": event} 
        )

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(result.to_dict())
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"errors": [{"message": str(e)}]})}
