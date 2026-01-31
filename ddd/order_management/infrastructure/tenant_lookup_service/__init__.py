import os
from ddd.order_management.bootstrap import (
    enums as infra_enums
)

INFRA_TYPE = os.getenv("ORDER_MANAGEMENT_INFRA_TYPE")

if INFRA_TYPE == infra_enums.InfraType.AWS.value:
    from .dynamodb_tenant_lookup_service import DynamodbTenantLookupService
else:
    from .tenant_lookup_service import TenantLookupService