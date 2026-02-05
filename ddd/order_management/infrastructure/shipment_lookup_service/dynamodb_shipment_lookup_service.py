import os
import boto3
from boto3.dynamodb.conditions import Key
from typing import Optional

class DynamodbShipmentLookupService:
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def get_tenant_id_by_tracking_ref(self, tracking_reference: str) -> Optional[str]:
        # Query the GSI instead of the main table
        response = self.table.query(
            IndexName='TrackingIndex',
            KeyConditionExpression=Key('tracking_reference').eq(tracking_reference),
            Limit=1
        )

        items = response.get('Items', [])
        print("DynamodbShipmentLookupService - get_tenant_id_by_tracking_ref - items:", items, tracking_reference)
        
        if not items:
            return None

        # Return the tenant_id directly from the projected attributes
        return items[0].get('tenant_id')
