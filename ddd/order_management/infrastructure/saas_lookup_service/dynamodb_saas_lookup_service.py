import boto3
import json
from botocore.exceptions import ClientError
from ddd.order_management.application import dtos

class DynamodbSaaSLookupService:
    def __init__(self, table_name: str):
        # Initialize the DynamoDB resource
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def get_tenant_config(self, tenant_id: str) -> dtos.TenantResponseDTO:
        try:
            # Perform a primary key lookup for the tenant_id
            response = self.table.get_item(
                Key={
                    'pk': f'TENANT#{tenant_id}',
                    'sk': 'CONFIG#SAAS'
                }
            )

        except ClientError as e:
            # Handle AWS service-side errors (e.g., throttling, access issues)
            raise Exception(f"Dynamodb SaasLookupService error: {e.response['Error']['Message']}")

        # DynamoDB get_item returns an empty dict if the key is not found
        item = response.get('Item')
        if not item:
            raise Exception(f"Tenant {tenant_id} not found")

        # In DynamoDB, 'configs' is typically stored as a Map (dict),
        # so native JSON parsing (json.loads) is usually unnecessary.
        configs = item.get('configs', {})

        # SAFETY CHECK: If it's a string, parse it. If it's already a dict, leave it.
        if isinstance(configs, str):
            try:
                configs = json.loads(configs)
            except json.JSONDecodeError:
                # Fallback if the string isn't valid JSON
                configs = {}


        return dtos.TenantResponseDTO(
            tenant_id=tenant_id,
            configs=configs
        )
