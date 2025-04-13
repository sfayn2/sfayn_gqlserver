from typing import Union
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
    shared
)
from ddd.order_management.domain import domain_service, events, exceptions

def handle_select_shipping_option(
        command: commands.SelectShippingOption, 
        uow: ports.UnitOfWorkAbstract,
        shipping_option_service: ports.ShippingOptionStrategyServiceAbstract,
        order_service: domain_service.OrderServiceAbstract
        ) -> Union[dtos.OrderResponseDTO, dtos.ResponseDTO]:
    try:
        with uow:

            order = uow.order.get(order_id=command.order_id)

            available_shipping_options = order_service.get_shipping_options(
                shipping_option_service=shipping_option_service(uow.vendor),
                order=order
            )

            order_w_shipping_option = order.select_shipping_option(
                                            command.shipping_details, 
                                            available_shipping_options
                                        )

            order_w_shipping_option_dto = mappers.OrderResponseMapper.to_dto(
                order=order_w_shipping_option,
                success=True,
                message="Order successfully selected shipping option."
            )

            uow.order.save(order_w_shipping_option)
            uow.commit()

    except (exceptions.InvalidOrderOperation, ValueError) as e:
        order_w_shipping_option_dto = shared.handle_invalid_order_operation(e)
    except Exception as e:
        order_w_shipping_option_dto = shared.handle_unexpected_error(f"Unexpected error during cart items checkout. {e}")

    return order_w_shipping_option_dto
