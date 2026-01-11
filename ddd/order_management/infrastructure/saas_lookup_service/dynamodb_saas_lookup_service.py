import boto3
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
                Key={'tenant_id': tenant_id}
            )
        except ClientError as e:
            # Handle AWS service-side errors (e.g., throttling, access issues)
            raise Exception(f"Database error: {e.response['Error']['Message']}")

        # DynamoDB get_item returns an empty dict if the key is not found
        item = response.get('Item')
        if not item:
            raise Exception(f"Tenant {tenant_id} not found")

        # In DynamoDB, 'configs' is typically stored as a Map (dict),
        # so native JSON parsing (json.loads) is usually unnecessary.
        configs = item.get('configs', {})

        return dtos.TenantResponseDTO(
            tenant_id=tenant_id,
            configs=configs
        )
