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
        uow: UnitOfWorkAbstract) -> dtos.ResponseDTO:
    try:
        with uow:

            order = uow.order.get(order_id=command.order_id)

            stock_validation_service.ensure_items_in_stock(order.line_items)

            offers = offer_service.evaluate_applicable_offers(order)
            order.apply_applicable_offers(offers)

            tax_results = tax_service.calculate_all_taxes(order)
            order.apply_tax_results(tax_results)

            order.place_order()

            uow.order.save(order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message="Order successfully placed order."
            )


    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)

