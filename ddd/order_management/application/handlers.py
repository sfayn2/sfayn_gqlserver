import uuid
from decimal import Decimal
from datetime import datetime
from ddd.order_management.application import commands, unit_of_work, helpers, queries
from ddd.order_management.domain import models, events, value_objects, enums, exceptions
from ddd.order_management.domain.services import order_service, offer_service, tax_service, shipping_option_service

def handle_place_order(command: commands.PlaceOrderCommand, uow: unit_of_work.DjangoOrderUnitOfWork):
    with uow:

        placed_order = order_service.place_order(
            customer_details=command.customer_details.to_domain(),
            shipping_address=command.shipping_address.to_domain(),
            shipping_details=command.shipping_details.to_domain(),
            coupons=[item.to_domain() for item in command.coupons],
            line_items=[item.to_domain() for item in command.line_items],
            offer_service=offer_service.OfferStrategyService(uow.vendor)
        )

        uow.order.save(placed_order)
        uow.commit()

        return placed_order

def handle_confirm_order(command: commands.ConfirmOrderCommand, uow: unit_of_work.DjangoOrderUnitOfWork):
    with uow:

        order = uow.order.get(order_id=command.order_id)
        if not order:
            raise exceptions.InvalidOrderOperation(f"Order id {command.order_id} not found.")

        payment_gateway = uow.payments.get_payment_gateway(command.payment_method)
        payment_details = payment_gateway.get_payment_details(command.transaction_id)

        confirmed_order = order_service.confirm_order(
            order=order,
            payment_details=payment_details
        )

        uow.order.save(confirmed_order)
        uow.commit()

        return confirmed_order


def handle_shipping_options(query: queries.ShippingOptionsQuery, uow: unit_of_work.DjangoOrderUnitOfWork):
    with uow:

        order = uow.order.get(order_id=query.order_id)

        shipping_options = order_service.get_shipping_options(
            shipping_option_service=shipping_option_service.ShippingOptionStrategyService(uow.vendor),
            order=order
        )

        return shipping_options

def handle_selection_shipping_options(command: commands.SelectShippingOption, uow: unit_of_work.DjangoOrderUnitOfWork):
    with uow:

        order = uow.order.get(order_id=command.order_id)

        available_shipping_options = order_service.get_shipping_options(
            shipping_option_service=shipping_option_service.ShippingOptionStrategyService(uow.vendor),
            order=order
        )

        order_w_shipping_option = order.select_shipping_option(
                                        command.shipping_details, 
                                        available_shipping_options
                                    )

        uow.order.save(order_w_shipping_option)
        uow.commit()

        return order_w_shipping_option


        

