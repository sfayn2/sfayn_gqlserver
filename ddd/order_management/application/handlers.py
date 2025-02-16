import uuid
from decimal import Decimal
from datetime import datetime
from ddd.order_management.application import commands, unit_of_work
from ddd.order_management.domain import models, events, value_objects, enums
from ddd.order_management.domain.services import order_service, offer_service, tax_service
from ddd.order_management.infrastructure import django_vendor_repository

def handle_place_order(command: commands.PlaceOrderCommand, uow: unit_of_work.DjangoOrderUnitOfWork):
    with uow:

        offer_svc = offer_service.OfferStrategyService(
            django_vendor_repository.DjangoVendorRepository()
        )

        placed_order = order_service.place_order(
            customer_details=command.customer_details.to_domain(),
            shipping_address=command.shipping_address.to_domain(),
            shipping_details=command.shipping_details.to_domain(),
            coupons=[item.to_domain() for item in command.coupons],
            line_items=[item.to_domain() for item in command.line_items],
            tax_service=tax_service.TaxStrategyService(),
            offer_service=offer_svc
        )


        event = events.OrderPlaced(
            order_id=placed_order.order_id,
            order_status=placed_order.order_status,
            customer_details=placed_order.customer_details,
            shipping_details=placed_order.shipping_details,
            line_items=placed_order.line_items,
            tax_details=placed_order.tax_details,
            tax_amount=placed_order.tax_amount,
            offer_details=placed_order.offer_details,
            total_discounts_fee=placed_order.total_discounts_fee,
            final_amount=placed_order.final_amount
        )

        uow.order.save(placed_order)
        uow.commit()

        #results, event
        return placed_order, event