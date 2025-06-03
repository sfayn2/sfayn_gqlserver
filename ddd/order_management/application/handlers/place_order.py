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


def handle_place_order(
        command: commands.PlaceOrderCommand, 
        tax_service:  TaxStrategyServiceAbstract,
        offer_service:  OfferStrategyServiceAbstract,
        stock_validation_service: StockValidationServiceAbstract,
        uow: UnitOfWorkAbstract) -> Union[dtos.OrderResponseDTO, dtos.ResponseDTO]:
    try:
        with uow:

            order = uow.order.get(order_id=command.order_id)

            stock_validation_service.ensure_items_in_stock(order.line_items)

            offers = offer_service.evaluate_applicable_offers(order)
            order.apply_applicable_offers(offers)

            tax_results = tax_service.calculate_all_taxes(order)
            order.apply_tax_results(tax_results)

            order.place_order()

            placed_order_dto =  mappers.OrderResponseMapper.to_dto(
                order=order,
                success=True,
                message="Order successfully placed order."
            )

            uow.order.save(order)
            uow.commit()


    except (exceptions.InvalidOrderOperation, ValueError) as e:
        placed_order_dto = shared.handle_invalid_order_operation(e)
    except Exception as e:
        placed_order_dto = shared.handle_unexpected_error(f"Unexpected error during place order {e}")

    return placed_order_dto

