from order_management import models as django_models
from ddd.order_management.application import dtos


# Improved error handling using .first() or try/except
class ShipmentLookupService:
    def get_context_by_tracking_ref(self, tracking_reference: str) -> dtos.ShipmentLookupContextDTO | None:
        try:
            # The select_related() method is added here to optimize performance (see #3)
            shipment = django_models.Shipment.objects.select_related('order').get(
                tracking_reference=tracking_reference
            )
            return dtos.ShipmentLookupContextDTO(
                tenant_id=shipment.order.tenant_id,
                order_id=shipment.order.order_id,
                tracking_reference=tracking_reference
            )
        except django_models.Shipment.DoesNotExist:
            # Handle the case where no shipment is found
            return None
