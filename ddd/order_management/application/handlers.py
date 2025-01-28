import uuid
from decimal import Decimal
from datetime import datetime
from ddd.order_management.application import commands, unit_of_work
from ddd.order_management.domain import models, events, value_objects, enums

def handle_checkout(command: commands.CheckoutCommand, uow: unit_of_work.DjangoOrderUnitOfWork):
    with uow:

        order = models.Order.create_draft_order(
            destination=command.address.to_domain(),
            customer_details=command.customer_details.to_domain(),
            line_items=[item.to_domain() for item in command.line_items]
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

def handle_place_order(command: commands.PlaceOrderCommand, uow: unit_of_work.DjangoOrderUnitOfWork):
    with uow:

        order = uow.order.get(command.order_id)

        if not order:
            raise ValueError(f"Order w ID {command.order_id} not found.")

        order.update_customer_details(command.customer_details.to_domain())
        order.update_shipping_details(command.shipping_details.to_domain())
        order.apply_coupon(command.coupons.to_domain())
        order.update_line_items([item.to_domain() for item in command.line_items])


        event = events.OrderPlaced(
            order_id=order.order_id,
            order_status=order.order_status,
            customer_details=order.customer_details,
            shipping_details=order.shipping_details,
            line_items=order.line_items,
            tax_details=order.tax_details,
            tax_amount=order.tax_amount,
            offer_details=order.offer_details,
            total_discounts_fee=order.total_discounts_fee,
            final_amount=order.final_amount
        )

        uow.order.save(order)
        uow.commit()

        #results, event
        return order, event