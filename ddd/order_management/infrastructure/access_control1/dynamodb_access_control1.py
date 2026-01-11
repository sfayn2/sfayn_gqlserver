from __future__ import annotations
import boto3, os
from boto3.dynamodb.conditions import Key
from typing import Optional
from ddd.order_management.domain import exceptions
from ddd.order_management.application import dtos

class DynamodbAccessControl1:
    def __init__(self, jwt_handler):
        self.jwt_handler = jwt_handler
        # Initialize DynamoDB resource
        table_name = os.getenv("DYNAMODB_TABLE_NAME")
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def get_user_context(self, token: str, request_tenant_id: str) -> dtos.UserContextDTO:
        identity_claims = self.jwt_handler.decode(token)
        user_ctx = dtos.UserContextDTO.model_validate(identity_claims)

        if user_ctx.tenant_id != request_tenant_id:
            raise exceptions.AccessControlException(
                f"Tenant mismatch token={user_ctx.tenant_id}, request={request_tenant_id}"
            )
        return user_ctx

    def ensure_user_is_authorized_for(
        self, 
        user_context: dtos.UserContextDTO, 
        required_permission: str, 
        required_scope: Optional[dict] = None
    ) -> bool:
        # Construct the query for the tenant and permission
        # Using begins_with on the Sort Key to find all scopes for this permission
        sort_key_prefix = f"{required_permission}#"
        
        response = self.table.query(
            KeyConditionExpression=Key('tenant_id').eq(user_context.tenant_id) & 
                                   Key('permission_codename_scope').begins_with(sort_key_prefix),
            # Filter for only active permissions
            FilterExpression="is_active = :active",
            ExpressionAttributeValues={":active": True}
        )

        items = response.get('Items', [])

        if not items:
            raise exceptions.AccessControlException("Access denied: permission not granted")

        # If a specific scope is required, validate against matching items
        if required_scope:
            for item in items:
                # DynamoDB Map types are returned as native Python dicts
                auth_scope = item.get('raw_scope', {})
                if all(auth_scope.get(k) == v for k, v in required_scope.items()):
                    return True
            raise exceptions.AccessControlException("Access denied: required scoped permission not found")

        return True
