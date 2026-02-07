import os
import boto3
from boto3.dynamodb.conditions import Key
from typing import Optional
from ddd.order_management.application import dtos

class DynamodbShipmentLookupService:
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def get_context_by_tracking_ref(self, tracking_reference: str) -> dtos.ShipmentLookupContextDTO | None:
        # Query the GSI instead of the main table
        response = self.table.query(
            IndexName='TrackingIndex',
            KeyConditionExpression=Key('tracking_reference').eq(tracking_reference),
            Limit=1
        )

        items = response.get('Items', [])
        
        if not items:
            return None

        return dtos.ShipmentLookupContextDTO(
            tenant_id=items[0].get('tenant_id'),
            order_id=items[0].get('order_id'),
            tracking_reference=tracking_reference
        )
