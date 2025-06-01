from __future__ import annotations
from typing import Union, List
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
    shared,
    queries
)
#from ddd.order_management.domain import repositories
#from ddd.order_management.domain.services.order import ports as order_ports
#from ddd.order_management.domain.services.shipping_option_strategies import ports as shipping_option_ports

def handle_shipping_options(
        query: queries.ShippingOptionsQuery, 
        uow: UnitOfWorkAbstract,
        shipping_option_service: ShippingOptionStrategyServiceAbstract) -> List[dtos.ShippingDetailsDTO]:
    with uow:

        order = uow.order.get(order_id=query.order_id)

        available_shipping_options = shipping_option_service(uow.vendor).get_shipping_options(
            order=order
        )

        shipping_options_dto = mappers.ShippingOptionsResponseMapper.to_dtos(available_shipping_options)

        return shipping_options_dto
