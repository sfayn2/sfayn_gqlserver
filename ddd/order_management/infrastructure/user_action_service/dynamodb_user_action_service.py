
from __future__ import annotations
import boto3
from datetime import datetime, UTC
from typing import Optional
from boto3.dynamodb.conditions import Key
from ddd.order_management.application import dtos

class DynamodbUserActionService:
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def save_action(self, user_action_data: dtos.UserActionDTO) -> None:
        # Generate a timestamp for the sort key to allow ordering
        now = datetime.now(UTC).isoformat()
        
        self.table.put_item(
            Item={
                "pk": f"ORDER#{user_action_data.order_id}",
                "sk": f"ACTION#{user_action_data.action}#{now}",
                "entity_type": "USER_ACTION",
                "order_id": user_action_data.order_id,
                "action": user_action_data.action,
                "performed_by": user_action_data.performed_by,
                "user_input": user_action_data.user_input,
                "executed_at": now
            }
        )

    def get_last_action(self, order_id: str, action: str) -> Optional[dtos.UserActionDTO]:
        # Querying with ScanIndexForward=False gives us descending order (newest first)
        # Limit=1 gives us only the most recent entry
        response = self.table.query(
            KeyConditionExpression=Key("pk").eq(f"ORDER#{order_id}") & 
                                   Key("sk").begins_with(f"ACTION#{action}#"),
            ScanIndexForward=False, 
            Limit=1
        )
        
        items = response.get("Items", [])
        if not items:
            return None

        last_action_log = items[0]
        return dtos.UserActionDTO(
            order_id=last_action_log["order_id"],
            action=last_action_log["action"],
            performed_by=last_action_log["performed_by"],
            user_input=last_action_log["user_input"]
        )
