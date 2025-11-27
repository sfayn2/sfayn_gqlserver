from pydantic import BaseModel, constr
from ddd.order_management.application import dtos
from .commands import Command, AddOrderCommand

class Command2(Command):
    tenant_id: str

class PublishAddOrderCommand(Command2):
    headers: dict
    raw_body: bytes
    request_path: str

class PublishShipmentUpdatesCommand(Command):
    headers: dict
    raw_body: bytes
    request_path: str
    saas_id: str

