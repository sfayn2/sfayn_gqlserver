from __future__ import annotations
from typing import Union, List
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
    shared,
    queries
)

def handle_list_shipping_options(
        query: queries.ListShippingOptionsQuery, 
        uow: UnitOfWorkAbstract,
        vendor_repo: VendorAbstract,
        access_control: AccessControlServiceAbstract,
        shipping_option_service: ShippingOptionStrategyServiceAbstract
) -> List[dtos.ShippingDetailsDTO]:

    with uow:

        order = uow.order.get(order_id=query.order_id)

        access_control.ensure_user_is_authorized_for(
            token=command.token,
            required_permission="list_shipping_options",
            required_scope={"customer_id": order.customer_details.customer_id }
        )

        vendor_shipping_options = vendor_repo.get_shipping_options(
                tenant_id=order.tenant_id, 
                vendor_id=order.vendor_id
            )
        available_shipping_options = shipping_option_service.get_applicable_shipping_options(
            order=order,
            vendor_shipping_options=vendor_shipping_options
        )

        response_dto = [mappers.ShippingDetailsMapper.to_dto(opt) for opt in available_shipping_options]
        #shipping_options_dto = mappers.ShippingOptionsResponseMapper.to_dtos(available_shipping_options)

        return response_dto
