from uuid import uuid4
from ddd.product_catalog.domain import commands
from ddd.product_catalog.app import unit_of_work
from ddd.product_catalog.domain import events


def handle_product_activate(command: commands.ActivateProductCommand, uow: unit_of_work.DjangoUnitOfWork):
    with uow:
        #domain_product = uow.product.get(product_id="e3bf4346-864a-4875-8ef3-ed3909f49e48")
        domain_product = uow.product.get(product_id=command.product_id)
        print(domain_product)
        #domain_product.activate()

        event = events.ProductActivated(
            product_id=domain_product.get_id(),
            name=domain_product.get_name(), 
            description=domain_product.get_desc(),
            category=domain_product.get_category()
        )

        uow.product.save(domain_product)
        uow.commit()

        print("Product activated ")

        return event


def log_activated_product(event: events.ProductActivated, uow: unit_of_work.DjangoUnitOfWork):
    # handle the event by logging the product activated
    print(f"Product Activated: {event.product_id} - {event.name} ({event.description} {event.category})")