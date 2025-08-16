from ddd.order_management.application import dtos
from .base import IntegrationEvent

class VendorDetailsUpdateIntegrationEvent(IntegrationEvent):
    data: dtos.VendorDetailsSnapshotDTO

class VendorCouponUpdateIntegrationEvent(IntegrationEvent):
    data: dtos.VendorCouponSnapshotDTO

class VendorOfferUpdateIntegrationEvent(IntegrationEvent):
    data: dtos.VendorOfferSnapshotDTO

class VendorShippingOptionUpdateIntegrationEvent(IntegrationEvent):
    data: dtos.VendorShippingOptionSnapshotDTO