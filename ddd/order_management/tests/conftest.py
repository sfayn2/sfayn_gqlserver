import os
from ddd.order_management.infrastructure.bootstrap import (
    enums as infra_enums
)

INFRA_TYPE = os.getenv("ORDER_MANAGEMENT_INFRA_TYPE")

if INFRA_TYPE == infra_enums.InfraType.AWS.value:
    pytest_plugins = ["ddd.order_management.infrastructure.bootstrap.bootstrap_aws", "ddd.order_management.tests.seed_aws"] 
else:
    pytest_plugins = ["ddd.order_management.infrastructure.bootstrap.bootstrap_onprem", "ddd.order_management.tests.seed_onprem"]


