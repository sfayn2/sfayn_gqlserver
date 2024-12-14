from ddd.product_catalog.app import message_bus, unit_of_work
from ddd.product_catalog.domain import commands

def test_product_created():
    uow = unit_of_work.DjangoUnitOfWork
    command = commands.CreateProductCommand(name="SmartPhone", price=100.00, category="Electronics")

    message_bus.handle(command, uow)

def test_activate_product():
    uow = unit_of_work.DjangoUnitOfWork()
    cmd = commands.ActivateProductCommand(
        product_id="e3bf4346-864a-4875-8ef3-ed3909f49e48"
    )

    message_bus.handle(cmd, uow)

