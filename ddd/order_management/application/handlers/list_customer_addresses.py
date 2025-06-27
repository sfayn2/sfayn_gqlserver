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
        customer_repo: CustomerAbstract,
) -> List[dtos.AddressDTO]:

    customer_addresses = customer_repo.get_shipping_addresses(
        customer_id=query.customer_id
    )

    response_dto = [mappers.AddressMapper.to_dto(addr) for addr in customer_addresses]

    return response_dto
