import os
from ddd.order_management.bootstrap import (
    enums as infra_enums
)
from .jwt_token_handler import JwtTokenHandler
from .access_control_service import AccessControlService

INFRA_TYPE = os.getenv("ORDER_MANAGEMENT_INFRA_TYPE")

if INFRA_TYPE == infra_enums.InfraType.AWS.value:
    from .dynamodb_access_control1 import DynamodbAccessControl1
else:
    from .access_control1 import AccessControl1