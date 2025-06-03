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
        coupon_validation: CouponValidationAbstract,
        uow: UnitOfWorkAbstract) -> Union[dtos.OrderResponseDTO, dtos.ResponseDTO]:
    try:
        with uow:

            order = uow.order.get(order_id=command.order_id)
            valid_coupon  = coupon_validation.ensure_coupon_is_valid(
                    coupon_code=command.coupon_code, 
                    vendor_id=order.vendor_id
                )
            order.apply_valid_coupon(coupon=valid_coupon)

            order_w_coupon_dto =  mappers.OrderResponseMapper.to_dto(
                order=order,
                success=True,
                message="Order successfully add coupon."
            )

            uow.order.save(order)
            uow.commit()


    except (exceptions.InvalidOrderOperation, ValueError) as e:
        order_w_coupon_dto = shared.handle_invalid_order_operation(e)
    except Exception as e:
        order_w_coupon_dto = shared.handle_unexpected_error(f"Unexpected error during add coupon {e}")

    return order_w_coupon_dto

