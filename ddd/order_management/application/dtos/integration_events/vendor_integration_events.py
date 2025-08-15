from ddd.order_management.application import dtos
from .base import IntegrationEvent

class VendorDetailsUpdateIntegrationEvent(IntegrationEvent):
    data: dtos.VendorDetailsSnapshotDTO