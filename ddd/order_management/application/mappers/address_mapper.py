from ddd.order_management.application import dtos
from ddd.order_management.domain import value_objects

class AddressMapper:
    @staticmethod
    def to_domain(address_dto: dtos.AddressDTO) -> value_objects.Address:
        return value_objects.Address(**address_dto.model_dump())