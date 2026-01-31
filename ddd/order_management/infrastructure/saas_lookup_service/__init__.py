import os
from ddd.order_management.bootstrap import (
    enums as infra_enums
)

INFRA_TYPE = os.getenv("ORDER_MANAGEMENT_INFRA_TYPE")

if INFRA_TYPE == infra_enums.InfraType.AWS.value:
    from .dynamodb_saas_lookup_service import DynamodbSaaSLookupService
else:
    from .saas_lookup_service import SaaSLookupService