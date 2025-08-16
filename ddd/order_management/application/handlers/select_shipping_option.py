from __future__ import annotations
from typing import Union
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
    shared
)
from ddd.order_management.domain import exceptions

def handle_select_shipping_option(
        command: commands.SelectShippingOptionCommand, 
        uow: UnitOfWorkAbstract,
        vendor_repo: VendorAbstract,
        access_control: AccessControl1Abstract,
        shipping_option_service: ShippingOptionStrategyServiceAbstract,
        ) -> dtos.ResponseDTO:
    try:
        with uow:

            order = uow.order.get(order_id=command.order_id)

            access_control.ensure_user_is_authorized_for(
                token=command.token,
                required_permission="select_shipping_option",
                required_scope={"customer_id": order.customer_details.customer_id }
            )

            vendor_shipping_options = vendor_repo.get_shipping_options(vendor_id=order.vendor_id)
            available_shipping_options = shipping_option_service.get_applicable_shipping_options(
                order=order,
                vendor_shipping_options=vendor_shipping_options
            )

            order_w_shipping_option = order.select_shipping_option(
                                            shipping_option=mappers.ShippingDetailsMapper.to_domain(command.shipping_details),
                                            shipping_options=available_shipping_options
                                        )

            uow.order.save(order_w_shipping_option)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message=f"Order {order_w_shipping_option.order_id} successfully selected shipping option."
            )

    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)

