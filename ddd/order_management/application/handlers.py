import uuid
from decimal import Decimal
from datetime import datetime
from ddd.order_management.application import commands, unit_of_work, helpers
from ddd.order_management.domain import models, events, value_objects, enums, exceptions
from ddd.order_management.domain.services import order_service, offer_service, payment_verify_service, tax_service

def handle_place_order(command: commands.PlaceOrderCommand, uow: unit_of_work.DjangoOrderUnitOfWork):
    with uow:

        offer_svc = offer_service.OfferStrategyService(uow.vendor)

        placed_order = order_service.place_order(
            customer_details=command.customer_details.to_domain(),
            shipping_address=command.shipping_address.to_domain(),
            shipping_details=command.shipping_details.to_domain(),
            coupons=[item.to_domain() for item in command.coupons],
            line_items=[item.to_domain() for item in command.line_items],
            tax_service=tax_service.TaxStrategyService(),
            offer_service=offer_svc
        )

        uow.order.save(placed_order)
        uow.commit()

        return placed_order

def handle_confirm_order(command: commands.ConfirmOrderCommand, uow: unit_of_work.DjangoOrderUnitOfWork):
    with uow:

        order = uow.order.get(order_id=command.order_id)
        if not order:
            raise exceptions.InvalidOrderOperation(f"Order id {order.order_id} not found.")

        payment_gateway = helpers.select_payment_gateway(uow, command.method)

        payment_verify_svc = payment_verify_service.PaymentVerifyService(
            payment_gateway
        )

        confirmed_order = order_service.confirm_order(
            payment_verify_service=payment_verify_svc,
            order=order,
            transaction_id=command.transaction_id
        )

        uow.order.save(confirmed_order)
        uow.commit()

        return confirmed_order
