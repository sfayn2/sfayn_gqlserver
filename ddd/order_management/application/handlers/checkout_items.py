from typing import Union, TYPE_CHECKING
from ddd.order_management.application import (
    mappers, 
    commands, 
    dtos, 
)

from ddd.order_management.domain import repositories
from ddd.order_management.domain.services.order import ports as order_ports
from ddd.order_management.domain.services.tax_strategies import ports as tax_ports

def handle_checkout_items(
        command: commands.CheckoutItemsCommand, 
        uow: repositories.UnitOfWorkAbstract,
        tax_service:  tax_ports.TaxStrategyServiceAbstract,
        order_service: order_ports.OrderServiceAbstract) -> dtos.OrderResponseDTO:
    with uow:

        draft_order = order_service.create_draft_order(
            customer_details=mappers.CustomerDetailsMapper.to_domain(command.customer_details),
            shipping_address=mappers.AddressMapper.to_domain(command.shipping_address),
            line_items=[mappers.LineItemMapper.to_domain(item) for item in command.line_items],
        )

        total_tax, details = tax_service.calculate_all_taxes(draft_order)
        draft_order.apply_taxes(total_tax, details)


        draft_order_dto = mappers.OrderResponseMapper.to_dto(
            order=draft_order,
            success=True,
            message="Cart items successfully checkout."
        )

        uow.order.save(draft_order)
        uow.commit()

        return draft_order_dto


