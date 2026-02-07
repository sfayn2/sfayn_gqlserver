from typing import Protocol
from ddd.order_management.application import dtos

class ShipmentLookupServiceAbstract(Protocol):
    """
    Defines the interface for interacting with shipment data to retrieve
    core information needed by the application layer, abstracting the
    underlying persistence logic.
    """

    def get_context_by_tracking_ref(self, tracking_reference: str) -> dtos.ShipmentLookupContextDTO | None:
        """
        Retrieves the tenant ID and order ID associated with a given tracking reference.

        Args:
            tracking_reference: The unique tracking identifier for the shipment.

        Returns:
            The tenant ID and order ID as a tuple of strings if found, otherwise None.
        """
        # This is the abstract method definition.
        # Implementation details (like Django ORM calls) are omitted.
        ...

