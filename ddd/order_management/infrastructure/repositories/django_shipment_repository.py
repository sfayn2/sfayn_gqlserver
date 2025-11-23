from order_management import models as django_models


# Improved error handling using .first() or try/except
class DjangoShipmentRepository:
    def get_tenant_id_by_tracking_ref(self, tracking_reference: str) -> str | None:
        try:
            # The select_related() method is added here to optimize performance (see #3)
            shipment = django_models.Shipment.objects.select_related('order').get(
                tracking_reference=tracking_reference
            )
            return shipment.order.tenant_id
        except django_models.Shipment.DoesNotExist:
            # Handle the case where no shipment is found
            return None
