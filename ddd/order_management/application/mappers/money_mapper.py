from dataclasses import asdict
from ddd.order_management.application import dtos
from ddd.order_management.domain import models, value_objects, enums

class MoneyMapper:

    @staticmethod
    def to_domain(dto: dtos.MoneyDTO) -> value_objects.Money:
        return value_objects.Money(**dto.model_dump())
