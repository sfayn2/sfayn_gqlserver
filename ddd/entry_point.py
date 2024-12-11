from app import unit_of_work, message_bus
from domain import commands

def test_product_created():
    uow = unit_of_work.DjangoUnitOfWork
    mb = message_bus.MessageBus()
    command = commands.CreateProductCommand(name="SmartPhone", price=100.00, category="Electronics")

    mb.handle(command, uow)