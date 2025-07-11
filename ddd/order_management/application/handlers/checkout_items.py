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
        customer_repo: CustomerAbstract,
        vendor_repo: VendorAbstract,
        address_validation_service: CustomerAddressValidationAbstract,
        stock_validation_service: StockValidationServiceAbstract,
        access_control: AccessControlServiceAbstract,
        order_service: OrderServiceAbstract) -> dtos.ResponseDTO:
    try:
        with uow:

            access_control.ensure_user_is_authorized_for(
                token=command.token,
                required_permission="checkout_items",
                required_scope={"customer_id": command.customer_id}
            )

            customer_details = customer_repo.get_customer_details(command.customer_id)

            #shipping_address = customer_repo.get_shipping_address(command.customer_id)
            address_validation_service.ensure_customer_address_is_valid(
                customer_id=command.customer_id,
                address=command.address
            )

            line_items = vendor_repo.get_line_items(command.vendor_id, command.product_skus)

            stock_validation_service.ensure_items_in_stock(line_items)


            draft_order = order_service.create_draft_order(
                customer_details=customer_details,
                shipping_address=mappers.AddressMapper.to_domain(command.address),
                line_items=line_items,
                tenant_id=user_ctx.tenant_id
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



