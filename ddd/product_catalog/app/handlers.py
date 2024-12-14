from ddd.product_catalog.domain import commands
from ddd.product_catalog.app import unit_of_work
from ddd.product_catalog.domain import events
from uuid import uuid4


def change_status_command(command: commands.ChangeStatusCommand, uow: unit_of_work.DjangoUnitOfWork):
    print('handle change status')

def handle_create_product(command: commands.CreateProductCommand, uow: unit_of_work.DjangoUnitOfWork):
    # handle the command to create a product
    product_id = str(uuid4())
    print("Create product handler here")
    event = events.ProductCreated(product_id, command.name, command.price, command.category)

    return event

def log_product_created(event: events.ProductCreated, uow: unit_of_work.DjangoUnitOfWork):
    # handle the event by logging the product created
    print(f"Product Created: {event.product_id} - {event.name} ({event.price} {event.category})")

def log_product_created2(event: events.ProductCreated, uow: unit_of_work.DjangoUnitOfWork):
    # handle the event by logging the product created
    print(f"Product Created2: {event.product_id} - {event.name} ({event.price} {event.category})")