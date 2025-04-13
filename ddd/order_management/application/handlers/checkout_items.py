
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
        order_service: domain_service.OrderServiceAbstract) -> dtos.OrderResponseDTO:
    with uow:

        draft_order = order_service.draft_order(
            customer_details=mappers.CustomerDetailsMapper.to_domain(command.customer_details),
            shipping_address=mappers.AddressMapper.to_domain(command.shipping_address),
            line_items=[mappers.LineItemMapper.to_domain(item) for item in command.line_items],
        )
        draft_order_dto = mappers.OrderResponseMapper.to_dto(
            order=draft_order,
            success=True,
            message="Cart items successfully checkout."
        )

        uow.order.save(draft_order)
        uow.commit()

        return draft_order_dto


