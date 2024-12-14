from ddd.product_catalog.app import unit_of_work, message_bus
from ddd.product_catalog.domain import commands

def test_product_created():
    uow = unit_of_work.DjangoUnitOfWork
    mb = message_bus.MessageBus()
    command = commands.CreateProductCommand(name="SmartPhone", price=100.00, category="Electronics")

    mb.handle(command, uow)

def test_activate_product():
    uow = unit_of_work.DjangoUnitOfWork()
    msg = message_bus.MessageBus()
    command = commands.ActivateProductCommand(product_id="e3bf4346-864a-4875-8ef3-ed3909f49e48")

    msg.handle(command, uow)

