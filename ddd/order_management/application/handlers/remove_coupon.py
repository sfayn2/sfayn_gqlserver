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


def handle_remove_coupon(
        command: commands.RemoveCouponCommand, 
        uow: UnitOfWorkAbstract,
        coupon_validation: CouponValidationAbstract,
        access_control: AccessControl1Abstract,
        user_ctx: dtos.UserContextDTO
) -> dtos.ResponseDTO:

    try:
        with uow:

            access_control.ensure_user_is_authorized_for(
                user_ctx,
                required_permission="remove_coupon",
                required_scope={"customer_id": user_ctx.sub }
            )

            order = uow.order.get(order_id=command.order_id, tenant_id=user_ctx.tenant_id)

            valid_coupon  = coupon_validation.ensure_coupon_is_valid(
                    tenant_id=order.tenant_id,
                    coupon_code=command.coupon_code, 
                    vendor_id=order.vendor_id
                )

            order.remove_coupon(coupon=valid_coupon)

            uow.order.save(order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message=f"Order {order.order_id} successfully remove coupon."
            )


    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)


