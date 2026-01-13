import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from ddd.order_management.domain import models, repositories, exceptions
from .aws_dynamodb_mappers import OrderDynamoMapper

class DynamoOrderRepositoryImpl(repositories.OrderAbstract):
    def __init__(self, table_name: str):
        super().__init__()
        self.table = boto3.resource("dynamodb").Table(table_name)


    def get(self, order_id: str, tenant_id: str) -> models.Order:
        try:
            # 1. Fetch the Header (Tenant Partition)
            # Note: Ensure keys match your 'pk/sk' lowercase casing
            header_response = self.table.get_item(
                Key={"pk": f"TENANT#{tenant_id}", "sk": f"ORDER#{order_id}"}
            )
            header_item = header_response.get("Item")
            
            if not header_item:
                raise exceptions.InvalidOrderOperation(f"Order {order_id} not found.")

            # 2. Fetch all related items (Order Partition)
            # This gets Lines, Shipments, and ShipmentItems in one trip
            related_response = self.table.query(
                KeyConditionExpression=Key("pk").eq(f"ORDER#{order_id}")
            )
            related_items = related_response.get("Items", [])

            # 3. Use the Mapper to assemble the full aggregate
            order_domain = OrderDynamoMapper.to_domain(header_item, related_items)
            
            # Store for tracking (DDD pattern)
            self.seen.add(order_domain)
            
            return order_domain

        except ClientError as e:
            raise exceptions.InvalidOrderOperation(str(e))

    def save(self, order: models.Order):
        try:
            # 1. Get all items from mapper (Header + Lines + Shipments)
            all_items = OrderDynamoMapper.to_dynamo(order)
            
            # 2. Extract the Header (Aggregate Root) for versioning
            # In your mapper, the header is the first item or the one with entity_type "ORDER"
            header_item = next(i for i in all_items if i.get("entity_type") == "ORDER")
            child_items = [i for i in all_items if i.get("entity_type") != "ORDER"]

            # 3. Prepare Versioning
            current_version = getattr(order, "_version", 1)
            header_item["version"] = current_version + 1 

            # 4. Save Header with Optimistic Locking
            # This ensures the Order Aggregate hasn't been changed by another process
            condition = "attribute_not_exists(pk) OR version = :expected_version"
            expression_values = {":expected_version": current_version}

            self.table.put_item(
                Item=header_item,
                ConditionExpression=condition,
                ExpressionAttributeValues=expression_values
            )

            # 5. Save all Children (Lines/Shipments)
            # We use batch_writer here because we already "locked" the aggregate via the Header
            if child_items:
                with self.table.batch_writer() as batch:
                    for child in child_items:
                        batch.put_item(Item=child)
            
            # Update domain version on success
            order._version = header_item["version"]

        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise exceptions.InvalidOrderOperation(
                    f"Order {order.order_id} was modified by another process."
                )
            raise exceptions.InvalidOrderOperation(f"Failed to save order: {str(e)}")

