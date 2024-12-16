import uuid
from decimal import Decimal
from ddd.product_catalog.domain import commands, models
from ddd.product_catalog.app import unit_of_work
from ddd.product_catalog.domain import events


def handle_product_activate(command: commands.ActivateProductCommand, uow: unit_of_work.DjangoUnitOfWork):
    with uow:
        domain_product = uow.product.get(product_id=command.product_id)
        domain_product.activate()
        #new_sku = models.VariantItem(
        #    _id=uuid.uuid4(),
        #    _sku="TH-0022-XL",
        #    _name="SIZE",
        #    _options="XL",
        #    _price=models.Money(Decimal(1), "SGD"),
        #    _stock=models.Stock(1),
        #    _default=False,
        #    _is_active=True
        #)
        #domain_product.add_variants(new_sku)
        #domain_product.deactivate_sku("TH-0022-XL")

        event = events.ProductActivated(
            product_id=domain_product.get_id(),
            name=domain_product.get_name(), 
            description=domain_product.get_desc(),
            category=domain_product.get_category()
        )

        uow.product.save(domain_product)
        uow.commit()

        print("Active product")

        return event


def log_activated_product(event: events.ProductActivated, uow: unit_of_work.DjangoUnitOfWork):
    # handle the event by logging the product activated
    print(f"Product Activated: {event.product_id} - {event.name} ({event.description} {event.category})")