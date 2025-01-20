import uuid
from decimal import Decimal
from datetime import datetime
from ddd.order_management.application import commands, unit_of_work
from ddd.order_management.domain import models, events, value_objects, enums

def handle_checkout(command: commands.CheckoutCommand, uow: unit_of_work.DjangoUnitOfWork):
    with uow:
        order = models.Order.create_draft_order(
            destination=command.address,
            customer_details=command.customer_details,
            line_items=command.line_items
        )

        event = events.ProductCheckedout(
            order_id=order.order_id,
            destination=order.destination,
            customer_details=order.customer_details,
            line_items=order.line_items
        )

        uow.order.save(order)
        uow.commit()

        #results, event
        return order, event