from __future__ import annotations
from typing import Dict, Any, Protocol
from ddd.order_management.application import dtos
# Import the domain model type
from ddd.order_management.domain import models

class ShippingProviderServiceAbstract(Protocol):
    """
    Port (Interface) that defines how the Application layer interacts with 
    any shipping coordination service, regardless of the underlying implementation.
    """
    #def resolve(cls, tenant_id: str, payload, headers) -> dtos.ShippingWebhookIntegrationEvent: ...
    def create_shipment(cls, tenant_id: str, shipment: models.Shipment) -> dtos.CreateShipmentResponseDTO: ...
    # The 'configure' and internal methods should not be part of the application port
