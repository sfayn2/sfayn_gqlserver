from dataclasses import asdict
from ddd.order_management.application import dtos
from ddd.order_management.domain import models, value_objects, enums

class CustomerDetailsMapper:

    @staticmethod
    def to_domain(dto: dtos.CustomerDetailsDTO) -> value_objects.CustomerDetails:
        return value_objects.CustomerDetails(**dto.model_dump())

