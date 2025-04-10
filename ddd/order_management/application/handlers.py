import uuid
from typing import List
from decimal import Decimal
from datetime import datetime
from ddd.order_management.application import commands, queries, ports, mapper, dtos
from ddd.order_management.domain import domain_service, events

def handle_place_order(
        command: commands.PlaceOrderCommand, 
        uow: ports.UnitOfWorkAbstract) -> dtos.OrderResponseDTO:
    with uow:

        order = uow.order.get(order_id=command.order_id)

        placed_order = order.place_order()
        placed_order_dto =  mapper.OrderResponseMapper.to_dto(
            placed_order, 
            success=True, 
            message="Order successfully placed order."
        )

        uow.order.save(placed_order)
        uow.commit()

        return placed_order_dto


def handle_confirm_order(
        command: commands.ConfirmOrderCommand, 
        uow: ports.UnitOfWorkAbstract, 
        payment_gateway_factory: ports.PaymentGatewayFactoryAbstract,
        order_service: domain_service.OrderServiceAbstract
    ) -> dtos.OrderResponseDTO:

    with uow:

        order = uow.order.get(order_id=command.order_id)

        payment_gateway = payment_gateway_factory.get_payment_gateway(command.payment_method)
        payment_details = payment_gateway.get_payment_details(command.transaction_id)

        confirmed_order = order_service.confirm_order(
            order=order,
            payment_details=payment_details
        )
        confirmed_order_dto = mapper.OrderResponseMapper.to_dto(
            confirmed_order, 
            success=True, 
            message="Order successfully confirmed."
        )

        uow.order.save(confirmed_order)
        uow.commit()

        return confirmed_order_dto



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

        shipping_options_dto = mapper.ShippingOptionsResponseMapper.to_dtos(shipping_options)

        return shipping_options_dto

def handle_select_shipping_option(
        command: commands.SelectShippingOption, 
        uow: ports.UnitOfWorkAbstract,
        shipping_option_service: ports.ShippingOptionStrategyServiceAbstract,
        order_service: domain_service.OrderServiceAbstract
        ) -> dtos.OrderResponseDTO:
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

        order_w_shipping_option_dto = mapper.OrderResponseMapper.to_dto(
            order_w_shipping_option, 
            success=True, 
            message = "Order successfully selected shipping option."
        )

        uow.order.save(order_w_shipping_option)
        uow.commit()

        return order_w_shipping_option_dto



def handle_checkout_items(
        command: commands.CheckoutItemsCommand, 
        uow: ports.UnitOfWorkAbstract,
        order_service: domain_service.OrderServiceAbstract) -> dtos.OrderResponseDTO:
    with uow:

        draft_order = order_service.draft_order(
            customer_details=command.customer_details.to_domain(),
            shipping_address=command.shipping_address.to_domain(),
            line_items=[item.to_domain() for item in command.line_items],
        )
        draft_order_dto = mapper.OrderResponseMapper.to_dto(
            draft_order, 
            success=True, 
            message = "Cart items successfully checkout."
        )

        uow.order.save(draft_order)
        uow.commit()

        return draft_order_dto




def handle_logged_order(
        event: events.OrderCancelled, 
        uow: ports.UnitOfWorkAbstract, 
        logging_service: ports.LoggingServiceAbstract):

    logging_service.log(f"Order has been canceled {event.order_id}")

def handle_email_canceled_order(
        event: events.OrderCancelled, 
        uow: ports.UnitOfWorkAbstract, 
        email_service: ports.EmailServiceAbstract):

    msg = f"Order has been canceled {event.order_id}"
    email_service.send_email(msg)

        

