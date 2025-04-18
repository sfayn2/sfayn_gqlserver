
from typing import Union
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
    shared
)
from ddd.order_management.domain import domain_service, events, exceptions

def handle_checkout_items(
        command: commands.CheckoutItemsCommand, 
        uow: ports.UnitOfWorkAbstract,
        draft_order_service: domain_service.DraftOrderServiceAbstract) -> dtos.OrderResponseDTO:
    with uow:

        draft_order = draft_order_service.create_draft_order(
            customer_details=mappers.CustomerDetailsMapper.to_domain(command.customer_details),
            shipping_address=mappers.AddressMapper.to_domain(command.shipping_address),
            line_items=[mappers.LineItemMapper.to_domain(item) for item in command.line_items],
        )
        draft_order.apply_taxes(tax_service.TAX_STRATEGIES)
        draft_order.calculate_final_amount()

        draft_order_dto = mappers.OrderResponseMapper.to_dto(
            order=draft_order,
            success=True,
            message="Cart items successfully checkout."
        )

        uow.order.save(draft_order)
        uow.commit()

        return draft_order_dto


