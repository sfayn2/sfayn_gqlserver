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
    def create_shipment(self, tenant_id: str, shipment: models.Shipment) -> dtos.CreateShipmentResponseDTO:
        """Orchestrates the creation of a shipment."""
        ...
    # The 'configure' and internal methods should not be part of the application port
