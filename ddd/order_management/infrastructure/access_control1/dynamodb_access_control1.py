from __future__ import annotations
import boto3, os, json
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

        # Normalize Keycloak's 'organization' claim or other iDps follow the same way w keycloak
        raw_orgs = identity_claims.get("organization", [])
        
        # Extract keys if it's a dict, otherwise treat as list
        allowed_tenants = list(raw_orgs.keys()) if isinstance(raw_orgs, dict) else list(raw_orgs)
        allowed_tenants = [str(t) for t in allowed_tenants]

        # SECURITY CHECK: Match the request to the allowed list
        if request_tenant_id not in allowed_tenants:
            #logger.error(f"Unauthorized: User {identity_claims.get('sub')} tried to access {request_tenant_id}")
            raise exceptions.AccessControlException(f"You do not have access to tenant: {request_tenant_id}")

        user_ctx = dtos.UserContextDTO.model_validate({
            "sub": identity_claims.get("sub"),
            "token_type": identity_claims.get("typ"),
            "tenant_id": request_tenant_id,  # Use the validated requested ID
            "roles": identity_claims.get("roles", []),
        })

        return user_ctx

    def ensure_user_is_authorized_for(
        self, 
        user_context: dtos.UserContextDTO, 
        required_permission: str, 
        required_scope: Optional[dict] = None
    ) -> bool:

        # 1. Match your Seed prefixes:
        # PK is usually "TENANT#<id>"
        # SK for users is usually "AUTH#USER#<id>"
        
        response = self.table.query(
            KeyConditionExpression=Key('pk').eq(f"TENANT#{user_context.tenant_id}") & 
                                   Key('sk').begins_with(f"AUTH#USER#{required_permission}") # Or your specific prefix
            ,
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
                auth_scope = item.get('scope', {})
                # FIX: If DynamoDB returned a stringified JSON, parse it into a dict
                if isinstance(auth_scope, str):
                    try:
                        auth_scope = json.loads(auth_scope)
                    except json.JSONDecodeError:
                        auth_scope = {}

                if all(auth_scope.get(k) == v for k, v in required_scope.items()):
                    return True
            raise exceptions.AccessControlException("Access denied: required scoped permission not found")

        return True
