import uuid
from decimal import Decimal
from datetime import datetime
from ddd.order_management.application import commands, queries, ports
from ddd.order_management.domain.services import order_service, offer_service, tax_service, shipping_option_service

def handle_place_order(
        command: commands.PlaceOrderCommand, 
        uow: ports.UnitOfWorkAbstract):
    with uow:

        order = uow.order.get(order_id=command.order_id)

        placed_order = order.place_order()

        uow.order.save(placed_order)
        uow.commit()

        return placed_order

def handle_confirm_order(
        command: commands.ConfirmOrderCommand, 
        uow: ports.UnitOfWorkAbstract, 
        payment_gateway_factory: ports.PaymentGatewayFactoryAbstract
    ):

    with uow:

        order = uow.order.get(order_id=command.order_id)

        payment_gateway = payment_gateway_factory.get_payment_gateway(command.payment_method)
        payment_details = payment_gateway.get_payment_details(command.transaction_id)

        confirmed_order = order_service.confirm_order(
            order=order,
            payment_details=payment_details
        )

        uow.order.save(confirmed_order)
        uow.commit()

        return confirmed_order


def handle_shipping_options(
        query: queries.ShippingOptionsQuery, 
        uow: ports.UnitOfWorkAbstract,
        shipping_option_service: ports.ShippingOptionStrategyServiceAbstract):
    with uow:

        order = uow.order.get(order_id=query.order_id)

        shipping_options = order_service.get_shipping_options(
            shipping_option_service=shipping_option_service(uow.vendor),
            order=order
        )

        return shipping_options

def handle_select_shipping_option(
        command: commands.SelectShippingOption, 
        uow: ports.UnitOfWorkAbstract,
        shipping_option_service: ports.ShippingOptionStrategyServiceAbstract
        ):
    with uow:

        order = uow.order.get(order_id=command.order_id)

        available_shipping_options = order_service.get_shipping_options(
            shipping_option_service=shipping_option_service(uow.vendor),
            order=order
        )

        order_w_shipping_option = order.select_shipping_option(
                                        command.shipping_details, 
                                        available_shipping_options
                                    )

        uow.order.save(order_w_shipping_option)
        uow.commit()

        return order_w_shipping_option

def handle_checkout_items(
        command: commands.CheckoutItemsCommand, 
        uow: ports.UnitOfWorkAbstract):
    with uow:

        draft_order = order_service.draft_order(
            customer_details=command.customer_details.to_domain(),
            shipping_address=command.shipping_address.to_domain(),
            line_items=[item.to_domain() for item in command.line_items],
        )

        uow.order.save(draft_order)
        uow.commit()

        return draft_order



        

