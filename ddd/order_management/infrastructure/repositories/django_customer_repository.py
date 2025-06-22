from __future__ import annotations
from typing import List
from ddd.order_management.domain import repositories, exceptions, value_objects
from order_management import models as django_snapshots
from ddd.order_management.infrastructure import django_mappers

class DjangoCustomerRepositoryImpl(repositories.CustomerAbstract):

    def get_customer_details(self, customer_id: str) -> value_objects.CustomerDetails:
        try:
            customer_details = django_snapshots.CustomerDetailsSnapshot.objects.get(
                customer_id=customer_id,
                is_active=True)
        except django_snapshots.CustomerDetailsSnapshot.DoesNotExist:
                raise exceptions.InvalidOrderOperation(f"Customer details for {customer_id} is not available.")

        return django_mappers.CustomerDetailsMapper.to_domain(customer_details)

    def get_shipping_addresses(self, customer_id: str) -> List[value_objects.Address]:
        customer_addresses = django_snapshots.CustomerAddressSnapshot.objects.filter(
            customer_id=customer_id,
            address_type="shipping",
            is_active=True)

        if not customer_addresses.exists():
            raise exceptions.InvalidOrderOperation(f"No available shipping address for Customer {customer_id}.")

        final_customer_address = []
        for address in customer_addresses:
            final_customer_address.append(
                django_mappers.AddressMapper.to_domain(address)
            )

        return final_customer_address

