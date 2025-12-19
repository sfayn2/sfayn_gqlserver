import boto3
from botocore.exceptions import ClientError
from ddd.order_management.domain import models, repositories, exceptions
from .aws_dynamodb_mappers import OrderDynamoMapper

class DynamoOrderRepositoryImpl(repositories.OrderAbstract):
    def __init__(self, table_name: str):
        super().__init__()
        self.table = boto3.resource("dynamodb").Table(table_name)

    def get(self, order_id: str, tenant_id: str) -> models.Order:
        try:
            response = self.table.get_item(
                Key={"PK": f"TENANT#{tenant_id}", "SK": f"ORDER#{order_id}"}
            )
            item = response.get("Item")
            if not item:
                raise exceptions.InvalidOrderOperation(f"Order {order_id} not found.")
            
            order_domain = OrderDynamoMapper.to_domain(item)
            # Store the current version for later comparison
            self.seen.add(order_domain)
            return order_domain
        except ClientError as e:
            raise exceptions.InvalidOrderOperation(str(e))

    def save(self, order: models.Order):
        try:
            current_version = order.version  # Assumes domain model has .version
            item = OrderDynamoMapper.to_dynamo(order)
            
            # Increment version for the NEXT state
            item["version"] = current_version + 1 

            # Optimistic Locking Logic
            condition = "attribute_not_exists(PK) OR version = :expected_version"
            expression_values = {":expected_version": current_version}

            self.table.put_item(
                Item=item,
                ConditionExpression=condition,
                ExpressionAttributeValues=expression_values
            )
            
            # Update domain model version on success
            order.version = item["version"]
            self.seen.add(order)

        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                # This error means someone else updated the record in the meantime
                raise exceptions.ConcurrencyException(
                    f"Order {order.order_id} was modified by another process."
                )
            raise exceptions.InvalidOrderOperation(f"Failed to save order: {str(e)}")
