from pydantic import BaseModel, constr
from ddd.order_management.application import dtos
from .commands import Command, AddOrderCommand

class Command2(Command):
    tenant_id: str

class PublishAddOrderCommand(Command2):
    headers: dict
    raw_body: bytes
    request_path: str

class PublishShipmentTrackerCommand(Command):
    headers: dict
    raw_body: bytes
    request_path: str

    #this can accept either saas_id or tenant_id depending on the webhook type
    tenant_id: str


#class PublishShipmentTrackerTenantCommand(Command2):
#    headers: dict
#    raw_body: bytes
#    request_path: str