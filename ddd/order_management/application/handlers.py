import uuid
from decimal import Decimal
from datetime import datetime
from ddd.order_management.application import commands, unit_of_work
from ddd.order_management.domain import models, events, value_objects, enums

def handle_checkout(command: commands.CheckoutCommand, uow: unit_of_work.DjangoUnitOfWork):
    with uow:
        order_details = models.Order(
            _order_id=uuid.uuid4(),
            _status=enums.OrderStatus.DRAFT.name,
            _date_created=datetime.now(),
            destination=command.address,
            customer_details=value_objects.CustomerDetails(
                first_name=command.first_name,
                last_name=command.last_name,
                email=command.email
            ),
            line_items=command.line_items
        )

        uow.order.save(order_details)
        uow.commit()