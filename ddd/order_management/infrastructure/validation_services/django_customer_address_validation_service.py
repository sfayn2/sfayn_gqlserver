from __future__ import annotations
import uuid
from typing import List, Union
from ddd.order_management.application import ports, dtos
from ddd.order_management.infrastructure import django_mappers
from ddd.order_management.domain import exceptions
from order_management import models as django_snapshots

class DjangoCustomerAddressValidationService(ports.CustomerAddressValidationServiceAbstract):

    def ensure_customer_address_is_valid(
        self, customer_id: str, address: dtos.AddressDTO
    ) -> value_objects.Address:

        try:
            customer_address = django_snapshots.CustomerAddressSnapshot.objects.get(
                customer_id=customer_id,
                street=address.street,
                city=address.city,
                postal_code=address.postal,
                country=address.country,
                state=address.state
            )
        except django_snapshots.CustomerAddressSnapshot.DoesNotExist:
            raise exceptions.AddressException(
                f"{address} is not valid address of Customer {customer_id}"
            )


