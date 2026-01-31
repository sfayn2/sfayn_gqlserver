import os
from dotenv import load_dotenv
from ddd.order_management.bootstrap import (
    enums as infra_enums
)

# Load environment variables from .env file
load_dotenv()

INFRA_TYPE = os.getenv("ORDER_MANAGEMENT_INFRA_TYPE")

if INFRA_TYPE == infra_enums.InfraType.AWS.value:
    pytest_plugins = ["ddd.order_management.bootstrap.bootstrap_aws", "ddd.order_management.tests.fixtures_aws"] 
else:
    #bootstrap onprem by default
    pytest_plugins = ["ddd.order_management.tests.fixtures_onprem"]


