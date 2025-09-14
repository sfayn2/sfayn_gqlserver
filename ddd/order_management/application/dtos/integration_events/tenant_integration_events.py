from ddd.order_management.application import dtos
from .base import IntegrationEvent

#TODO
class TenantWorkflowUpdateIntegrationEvent(IntegrationEvent):
    pass
    #data: dtos.VendorDetailsSnapshotDTO

class TenantRolemapUpdateIntegrationEvent(IntegrationEvent):
    pass
    #data: dtos.VendorDetailsSnapshotDTO

class TenantCreateOrderIntegrationEvent(IntegrationEvent):
    pass
    #data: dtos.VendorDetailsSnapshotDTO
