from __future__ import annotations
from ddd.order_management.application import dtos
from ddd.order_management.domain import models, value_objects

class AddressMapper:

    @staticmethod
    def to_domain(address: dtos.AddressDTO) -> value_objects.Address:
        return value_objects.Address(
            line1=address.line1,
            city=address.city,
            country=address.country,
            line2=address.line2,
            state=address.state,
            postal=address.postal
        )