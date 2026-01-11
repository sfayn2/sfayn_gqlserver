import os
from ddd.order_management.infrastructure.bootstrap import (
    enums as infra_enums
)

INFRA_TYPE = os.getenv("ORDER_MANAGEMENT_INFRA_TYPE")

if INFRA_TYPE == infra_enums.InfraType.AWS.value:
    from .dynamodb_shipment_lookup_service import DynamodbShipmentLookupService
else:
    from .shipment_lookup_service import ShipmentLookupService