from __future__ import annotations
from typing import Union, TYPE_CHECKING
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
    shared
)
from ddd.order_management.domain import exceptions
#if TYPE_CHECKING:
#    from ddd.order_management.domain import repositories
#    from ddd.order_management.domain.services.order import ports as order_ports
#    from ddd.order_management.domain.services.tax_strategies import ports as tax_ports
#    from ddd.order_management.domain.services.offer_strategies import ports as offer_ports


def handle_place_order(
        command: commands.PlaceOrderCommand, 
        tax_service:  TaxStrategyServiceAbstract,
        offer_service:  OfferStrategyServiceAbstract,
        uow: UnitOfWorkAbstract) -> Union[dtos.OrderResponseDTO, dtos.ResponseDTO]:
    try:
        with uow:

            order = uow.order.get(order_id=command.order_id)

            offers = offer_service.evaluate_applicable_offers(order)
            order.apply_applicable_offers(offers)

            tax_results = tax_service.calculate_all_taxes(order)
            order.apply_tax_results(tax_results)

            placed_order = order.place_order()


            placed_order_dto =  mappers.OrderResponseMapper.to_dto(
                order=placed_order,
                success=True,
                message="Order successfully placed order."
            )

            uow.order.save(placed_order)
            uow.commit()


    except (exceptions.InvalidOrderOperation, ValueError) as e:
        placed_order_dto = shared.handle_invalid_order_operation(e)
    except Exception as e:
        placed_order_dto = shared.handle_unexpected_error(f"Unexpected error during place order {e}")

    return placed_order_dto

