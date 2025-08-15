from ddd.order_management.application import dtos
from .base import IntegrationEvent

class ProductUpdateIntegrationEvent(IntegrationEvent):
    data: dtos.VendorProductSnapshotDTO


