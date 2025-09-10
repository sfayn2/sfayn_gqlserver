from pydantic import BaseModel, constr
from ddd.order_management.application import dtos
from .commands import Command

# ----------------
# Applicable to Webhook APIs / Integration events
# -----------
#class Command(BaseModel, frozen=True):
#
#    @property
#    def step_name(self) -> str:
#        return self.__class__.__name__.replace("Command", "").lower()

class Command2(Command):
    event_type: str

# {
#    "event_type": "events.ProductUpdateEvent",
#    "tenant_id": "tenant1",
#    "data": { ... }
# }
class PublishProductUpdateCommand(Command2):
    data: dtos.VendorProductSnapshotDTO

class PublishVendorDetailsUpdateCommand(Command2):
    data: dtos.VendorDetailsSnapshotDTO

class PublishVendorCouponUpdateCommand(Command2):
    data: dtos.VendorCouponSnapshotDTO

class PublishVendorOfferUpdateCommand(Command2):
    data: dtos.VendorOfferSnapshotDTO

class PublishVendorShippingOptionUpdateCommand(Command2):
    data: dtos.VendorShippingOptionSnapshotDTO

class PublishVendorPaymentOptionUpdateCommand(Command2):
    data: dtos.VendorPaymentOptionSnapshotDTO

class PublishVendorTaxOptionUpdateCommand(Command2):
    data: dtos.VendorTaxOptionSnapshotDTO