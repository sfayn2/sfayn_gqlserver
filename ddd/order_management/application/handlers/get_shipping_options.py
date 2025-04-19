from typing import Union, List
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
    shared,
    queries
)
from ddd.order_management.domain.services.order import ports as order_ports
from ddd.order_management.domain.services.shipping_option_strategies import ports as shipping_option_ports

def handle_shipping_options(
        query: queries.ShippingOptionsQuery, 
        uow: ports.UnitOfWorkAbstract,
        shipping_option_service: shipping_option_ports.ShippingOptionStrategyServiceAbstract,
        order_service: order_ports.OrderServiceAbstract) -> List[dtos.ShippingDetailsDTO]:
    with uow:

        order = uow.order.get(order_id=query.order_id)

        shipping_options = order_service.get_shipping_options(
            shipping_option_service=shipping_option_service(uow.vendor),
            order=order
        )

        shipping_options_dto = mappers.ShippingOptionsResponseMapper.to_dtos(shipping_options)

        return shipping_options_dto
