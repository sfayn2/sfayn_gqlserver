from typing import Union, List
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
    shared,
    queries
)
from ddd.order_management.domain import domain_service, events, exceptions

def handle_shipping_options(
        query: queries.ShippingOptionsQuery, 
        uow: ports.UnitOfWorkAbstract,
        shipping_option_service: ports.ShippingOptionStrategyServiceAbstract,
        order_service: domain_service.OrderServiceAbstract) -> List[dtos.ShippingDetailsDTO]:
    with uow:

        order = uow.order.get(order_id=query.order_id)

        shipping_options = order_service.get_shipping_options(
            shipping_option_service=shipping_option_service(uow.vendor),
            order=order
        )

        shipping_options_dto = mappers.ShippingOptionsResponseMapper.to_dtos(shipping_options)

        return shipping_options_dto
