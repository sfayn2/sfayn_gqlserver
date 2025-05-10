from typing import Union
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
    shared
)
from ddd.order_management.domain import repositories, exceptions
from ddd.order_management.domain.services.order import ports as order_ports

def handle_confirm_order(
        command: commands.ConfirmOrderCommand, 
        uow: repositories.UnitOfWorkAbstract, 
        payment_gateway_factory: ports.PaymentGatewayFactoryAbstract,
        order_service: order_ports.OrderServiceAbstract
    ) -> Union[dtos.OrderResponseDTO, dtos.ResponseDTO]:

    try:

        with uow:

            order = uow.order.get(order_id=command.order_id)

            payment_gateway = payment_gateway_factory.get_payment_gateway(command.payment_method)
            payment_details = payment_gateway.get_payment_details(command.transaction_id)

            confirmed_order = order_service.confirm_order(
                order=order,
                payment_details=payment_details
            )

            confirmed_order_dto = mappers.OrderResponseMapper.to_dto(
                confirmed_order,
                success=True,
                message="Order successfully confirmed."
            )
            uow.order.save(confirmed_order)
            uow.commit()
                


    except (exceptions.InvalidOrderOperation, ValueError) as e:
        confirmed_order_dto = shared.handle_invalid_order_operation(e)
    except Exception as e:
        confirmed_order_dto = shared.handle_unexpected_error(f"Unexpected error during order confirmation. {e}")

    return confirmed_order_dto

