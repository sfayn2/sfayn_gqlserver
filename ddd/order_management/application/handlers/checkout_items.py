from __future__ import annotations
from typing import Union, TYPE_CHECKING
from ddd.order_management.application import (
    mappers, 
    commands, 
    dtos, 
)

def handle_checkout_items(
        command: commands.CheckoutItemsCommand, 
        uow: UnitOfWorkAbstract,
        tax_service:  TaxStrategyServiceAbstract,
        product_vendor_validation_service: ProductVendorValidationServiceAbstract,
        order_service: OrderServiceAbstract) -> dtos.OrderResponseDTO:
    with uow:

        line_items = [mappers.LineItemMapper.to_domain(item) for item in command.line_items]
        product_vendor_validation_service.ensure_line_items_vendor_is_valid(items=line_items)

        draft_order = order_service.create_draft_order(
            customer_details=mappers.CustomerDetailsMapper.to_domain(command.customer_details),
            shipping_address=mappers.AddressMapper.to_domain(command.shipping_address),
            line_items=line_items
        )

        tax_results = tax_service.calculate_all_taxes(draft_order)
        draft_order.apply_tax_results(tax_results)


        draft_order_dto = mappers.OrderResponseMapper.to_dto(
            order=draft_order,
            success=True,
            message="Cart items successfully checkout."
        )

        uow.order.save(draft_order)
        uow.commit()

        return draft_order_dto


