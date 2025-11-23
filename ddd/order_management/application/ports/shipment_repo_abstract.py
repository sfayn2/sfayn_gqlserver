from typing import Protocol

class ShipmentRepositoryAbstract(Protocol):
    """
    Defines the interface for interacting with shipment data to retrieve
    core information needed by the application layer, abstracting the
    underlying persistence logic.
    """

    def get_tenant_id_by_tracking_ref(self, tracking_reference: str) -> str | None:
        """
        Retrieves the tenant ID associated with a given tracking reference.

        Args:
            tracking_reference: The unique tracking identifier for the shipment.

        Returns:
            The tenant ID as a string if found, otherwise None.
        """
        # This is the abstract method definition.
        # Implementation details (like Django ORM calls) are omitted.
        ...

