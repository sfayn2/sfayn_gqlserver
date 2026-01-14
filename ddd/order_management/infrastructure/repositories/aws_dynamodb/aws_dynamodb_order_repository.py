import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from ddd.order_management.domain import models, repositories, exceptions
from .aws_dynamodb_mappers import OrderDynamoMapper

class OrderAggregateConflictException(Exception):
    def __init__(self, order_id: str, version: int):
        self.order_id = order_id
        self.version = version
        super().__init__(
            f"Action failed for Order '{order_id}'. This order was recently updated "
            f"by another process (expected version {version}). Please refresh and try again."
        )


class DynamoOrderRepositoryImpl(repositories.OrderAbstract):
    def __init__(self, table_name: str):
        super().__init__()
        self.table = boto3.resource("dynamodb").Table(table_name)
        self.table_name = table_name
        # We need the client for transactions
        self.client = self.table.meta.client


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
            all_items = OrderDynamoMapper.to_dynamo(order)
            
            header_item = next(i for i in all_items if i.get("entity_type") == "ORDER")
            child_items = [i for i in all_items if i.get("entity_type") != "ORDER"]

            current_version = getattr(order, "_version", 1)
            new_version = current_version + 1
            header_item["version"] = new_version

            # 1. Build the Transaction Actions
            transact_items = []

            # Add the Header with Optimistic Locking
            transact_items.append({
                'Put': {
                    'TableName': self.table_name,
                    'Item': header_item,
                    'ConditionExpression': "attribute_not_exists(pk) OR version = :expected",
                    'ExpressionAttributeValues': {':expected': current_version}
                }
            })

            # Add all children to the same transaction
            for child in child_items:
                transact_items.append({
                    'Put': {
                        'TableName': self.table_name,
                        'Item': child
                    }
                })

            # 2. Execute Atomically (All or Nothing)
            # Max 100 items per transaction in DynamoDB
            self.client.transact_write_items(TransactItems=transact_items)
            
            order._version = new_version

        except ClientError as e:
            code = e.response['Error']['Code']
            # Transactional lock failures return TransactionCanceledException
            if code == 'TransactionCanceledException':
                reasons = e.response['CancellationReasons']
                if reasons[0]['Code'] == 'ConditionalCheckFailed':
                    raise OrderAggregateConflictException(
                            order_id=order.order_id, 
                            version=order._version
                        )


