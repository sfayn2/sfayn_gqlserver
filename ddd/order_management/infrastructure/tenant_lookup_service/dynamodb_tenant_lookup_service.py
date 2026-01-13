import boto3
import json
from botocore.exceptions import ClientError
from ddd.order_management.application import dtos

class DynamodbTenantLookupService:
    def __init__(self, table_name: str ):
        # Initialize the DynamoDB resource
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def get_tenant_config(self, tenant_id: str) -> dtos.TenantResponseDTO:
        try:
            # Equivalent to django_models.TenantConfig.objects.get(tenant_id=tenant_id)
            response = self.table.get_item(
                Key={
                    'pk': f'TENANT#{tenant_id}',
                    'sk': 'CONFIG#TENANT'
                }
            )
        except ClientError as e:
            raise Exception(f"Dynamodb TenantLookupService error: {e.response['Error']['Message']}")

        item = response.get('Item')
        if not item:
            raise Exception(f"Tenant {tenant_id} not found")

        # DynamoDB maps ('M') or lists ('L') are returned as native Python dicts/lists,
        # so json.loads() is typically no longer needed if stored as a Document.
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
