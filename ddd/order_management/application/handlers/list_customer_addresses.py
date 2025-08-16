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

def handle_list_customer_addresses(
        query: queries.ListCustomerAddressesQuery, 
        uow: UnitOfWorkAbstract,
        access_control: AccessControl1Abstract,
        customer_repo: CustomerAbstract,
) -> List[dtos.AddressDTO]:

    user_ctx = access_control.ensure_user_is_authorized_for(
        token=query.token,
        required_permission="list_customer_addresses",
        required_scope={"customer_id": query.customer_id }
    )

    customer_addresses = customer_repo.get_shipping_addresses(
        tenant_id=user_ctx.tenant_id,
        customer_id=query.customer_id
    )


    response_dto = [mappers.AddressMapper.to_dto(addr) for addr in customer_addresses]

    return response_dto
