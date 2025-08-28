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

def handle_list_payment_options(
        query: queries.ListPaymentOptionsQuery, 
        uow: UnitOfWorkAbstract,
        vendor_repo: VendorAbstract,
        access_control: AccessControl1Abstract,
        payment_service: PaymentService
) -> List[dtos.PaymentOptionDTO]:

    with uow:

        order = uow.order.get(order_id=query.order_id)

        access_control.ensure_user_is_authorized_for(
            token=command.token,
            required_permission="list_payment_options",
            required_scope={"customer_id": order.customer_details.customer_id }
        )

        vendor_payment_options = vendor_repo.get_payment_options(
                tenant_id=order.tenant_id, 
                vendor_id=order.vendor_id
            )
        available_payment_options = payment_service.get_applicable_payment_options(
            order=order,
            vendor_payment_options=vendor_payment_options
        )

        #dto
        return available_payment_options

