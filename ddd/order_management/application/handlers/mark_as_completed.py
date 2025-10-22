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


def handle_mark_as_completed(
        command: commands.CompleteOrderCommand, 
        access_control_factory: callable[[str], AccessControl1Abstract],
        user_ctx: dtos.UserContextDTO,
        workflow_service: WorkflowService,
        uow: UnitOfWorkAbstract) -> dtos.ResponseDTO:
    try:
        with uow:
            access_control = access_control_factory(user_ctx.tenant_id)

            access_control.ensure_user_is_authorized_for(
                user_ctx,
                required_permission="mark_as_completed",
                required_scope={"role": ["vendor"] }
            )

            order = uow.order.get(order_id=command.order_id, tenant_id=user_ctx.tenant_id)
            workflow_service.mark_step_done(
                order_id=order.order_id,
                current_step=command.step_name,
                performed_by=user_ctx.sub)
            workflow_service.all_required_workflows_for_stage_done(
                order_id, 
                enums.OrderStatus.SHIPPED
            )
            order.mark_as_completed()

            uow.order.save(order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message=f"Order {order.order_id} successfully mark as completed."
            )


    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)

