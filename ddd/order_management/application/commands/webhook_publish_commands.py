from pydantic import BaseModel, constr
from ddd.order_management.application import dtos
from .commands import Command, AddOrderCommand

class Command2(Command):
    tenant_id: str

# {
#    "event_type": "events.ProductUpdateEvent",
#    "tenant_id": "tenant1",
#    "data": { ... }
# }

class PublishAddOrderCommand(Command2):
    #data: dtos.AddOrderDTO
    headers: dict
    raw_body: bytes
    request_path: str

class PublishShipmentUpdatesCommand(Command2):
    headers: dict
    raw_body: bytes
    request_path: str

