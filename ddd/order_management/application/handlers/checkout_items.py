from __future__ import annotations
from typing import Union, TYPE_CHECKING
from ddd.order_management.domain import exceptions
from ddd.order_management.application import (
    mappers, 
    commands, 
    dtos, 
    shared
)

def handle_checkout_items(
        command: commands.CheckoutItemsCommand, 
        uow: UnitOfWorkAbstract,
        product_vendor_validation_service: ProductVendorValidationServiceAbstract,
        order_service: OrderServiceAbstract) -> dtos.ResponseDTO:
    try:
        with uow:

            customer_details = mappers.CustomerDetailsMapper.to_domain(command.customer_details)
            shipping_address = mappers.AddressMapper.to_domain(command.shipping_address)
            line_items = [mappers.LineItemMapper.to_domain(item) for item in command.line_items]

            product_vendor_validation_service.ensure_line_items_vendor_is_valid(items=line_items)

            draft_order = order_service.create_draft_order(
                customer_details=customer_details,
                shipping_address=shipping_address,
                line_items=line_items
            )

            uow.order.save(draft_order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message="Cart items successfully checkout."
            )

    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)



