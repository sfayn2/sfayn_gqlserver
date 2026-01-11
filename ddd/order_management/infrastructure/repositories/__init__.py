import os
from ddd.order_management.infrastructure.bootstrap import (
    enums as infra_enums
)

INFRA_TYPE = os.getenv("ORDER_MANAGEMENT_INFRA_TYPE")

if INFRA_TYPE == infra_enums.InfraType.AWS.value:
    from .aws_dynamodb.aws_dynamodb_order_repository import DynamoOrderRepositoryImpl
    from .aws_dynamodb.aws_dynamodb_uow import DynamoOrderUnitOfWork
else:
    from .onprem_django.django_order_repository import DjangoOrderRepositoryImpl
    from .onprem_django.unit_of_work import DjangoOrderUnitOfWork