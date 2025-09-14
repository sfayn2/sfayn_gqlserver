from pydantic import BaseModel, constr
from ddd.order_management.application import dtos
from .commands import Command

class Command2(Command):
    event_type: str

# {
#    "event_type": "events.ProductUpdateEvent",
#    "tenant_id": "tenant1",
#    "data": { ... }
# }

#TODO data
class PublishTenantWorkflowUpdateCommand(Command2):
    pass
    #data: dtos.VendorProductSnapshotDTO

class PublishTenantRolemapUpdateCommand(Command2):
    pass
    #data: dtos.VendorProductSnapshotDTO

class PublishTenantCreateOrderCommand(Command2):
    pass
    #data: dtos.VendorProductSnapshotDTO