from __future__ import annotations
from dataclasses import asdict
from ddd.order_management.application import dtos
from ddd.order_management.domain import models

class AddressMapper:

    @staticmethod
    def to_dto(address: value_objects.Address) -> dtos.AddressDTO:
        return dtos.AddressDTO(**asdict(address))