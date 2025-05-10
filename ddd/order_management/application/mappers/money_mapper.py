from ddd.order_management.application import dtos
from ddd.order_management.domain import value_objects

class MoneyMapper:
    @staticmethod
    def to_domain(money_dto: dtos.MoneyDTO) -> value_objects.Money:
        return value_objects.Money(**money_dto.model_dump())