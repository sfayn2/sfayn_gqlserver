from typing import Union
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
    shared
)
from ddd.order_management.domain import exceptions, repositories
from ddd.order_management.domain.services.order import ports as order_ports
from ddd.order_management.domain.services.tax_strategies import ports as tax_ports
from ddd.order_management.domain.services.offer_strategies import ports as offer_ports


def handle_place_order(
        command: commands.PlaceOrderCommand, 
        order_service: order_ports.OrderServiceAbstract,
        tax_service:  tax_ports.TaxStrategyServiceAbstract,
        offer_service:  offer_ports.OfferStrategyServiceAbstract,
        uow: repositories.UnitOfWorkAbstract) -> Union[dtos.OrderResponseDTO, dtos.ResponseDTO]:
    try:
        with uow:

            order = uow.order.get(order_id=command.order_id)

            placed_order = order_service.place_order(order)

            offers = offer_service.get_final_offers(placed_order)
            placed_order.apply_offers(offers)

            tax_results = tax_service.calculate_all_taxes(placed_order)
            placed_order.apply_tax_results(tax_results)

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

