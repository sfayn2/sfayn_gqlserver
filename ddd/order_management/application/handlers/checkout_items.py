from __future__ import annotations
from typing import Union, TYPE_CHECKING
from ddd.order_management.domain import exceptions
from ddd.order_management.application import (
    mappers, 
    commands, 
    dtos, 
    shared
)

def handle_checkout_items(
        command: commands.CheckoutItemsCommand, 
        uow: UnitOfWorkAbstract,
        vendor_repo: VendorAbstract,
        stock_validation: StockValidationAbstract,
        access_control: AccessControl1Abstract,
        order_service: OrderServiceAbstract) -> dtos.ResponseDTO:
    try:
        with uow:

            user_ctx = access_control.get_user_context(command.token)
            access_control.ensure_user_is_authorized_for(
                user_ctx,
                required_permission="checkout_items"
            )
            tenant_id = user_ctx.tenant_id
            command.customer_details.customer_id = user_ctx.sub

            # Decision: allow user to fill in customer details + address in front end
            #customer_details = customer_repo.get_customer_details(command.customer_id)

            #address_validation_service.ensure_customer_address_is_valid(
            #    customer_id=command.customer_id,
            #    address=command.address
            #)

            stock_validation.ensure_items_in_stock(
                tenant_id,
                command.product_skus
            )

            vendor_line_items = vendor_repo.get_line_items(
                tenant_id,
                command.product_skus
            )

            draft_order = order_service.create_draft_order(
                customer_details=mappers.CustomerDetailsMapper.to_domain(command.customer_details),
                shipping_address=mappers.AddressMapper.to_domain(command.address),
                line_items=vendor_line_items,
                tenant_id=tenant_id
            )


            uow.order.save(draft_order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message="Cart items successfully checkout."
            )

    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)



