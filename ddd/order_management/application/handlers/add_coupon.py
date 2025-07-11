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


def handle_add_coupon(
        command: commands.AddCouponCommand, 
        coupon_validation_service: CouponValidationServiceAbstract,
        uow: UnitOfWorkAbstract,
        access_control: AccessControlServiceAbstract
) -> dtos.ResponseDTO:

    try:
        with uow:

            order = uow.order.get(order_id=command.order_id)

            access_control.ensure_user_is_authorized_for(
                token=command.token,
                required_permission="add_coupon",
                required_scope={"tenant_id": order.tenant_id, "customer_id": order.customer_details.customer_id}
            )

            valid_coupon  = coupon_validation_service.ensure_coupon_is_valid(
                    coupon_code=command.coupon_code, 
                    vendor_id=order.vendor_id
                )
            order.apply_valid_coupon(coupon=valid_coupon)

            uow.order.save(order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message=f"Order {order.order_id} successfully add coupon."
            )


    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)


