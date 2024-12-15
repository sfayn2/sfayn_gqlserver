from ddd.product_catalog.app import message_bus, unit_of_work
from ddd.product_catalog.domain import commands

def test_product_created():
    uow = unit_of_work.DjangoUnitOfWork
    command = commands.CreateProductCommand(name="SmartPhone", price=100.00, category="Electronics")

    message_bus.handle(command, uow)

def test_activate_product():
    uow = unit_of_work.DjangoUnitOfWork()
    cmd = commands.ActivateProductCommand(
        product_id="56d562a7-d017-42bb-9da2-45effd5584cd"
    )

    message_bus.handle(cmd, uow)

