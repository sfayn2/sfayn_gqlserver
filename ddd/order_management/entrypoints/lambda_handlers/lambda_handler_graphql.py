import json
from ddd.order_management.infrastructure.bootstrap import bootstrap_aws
from ddd.order_management.entrypoints.graphql.schema import schema

def handler(event, context):
    try:

        body = json.loads(event.get("body", "{}"))
        #print("Received event body:", body)
        
        # Execute with context_value so info.context is populated
        result = schema.execute(
            body.get("query"),
            variable_values=body.get("variables", {}),
            # Pass the event as context so resolvers can see headers/cookies
            context_value={"request_event": event} 
        )


        # Graphene results need to be manually formatted
        response_payload = {}
        
        if result.data is not None:
            response_payload["data"] = result.data
        
        if result.errors:
            # Format errors into a list of strings or dicts
            response_payload["errors"] = [{"message": str(e)} for e in result.errors]

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(response_payload)
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"errors": [{"message": str(e)}]})}
