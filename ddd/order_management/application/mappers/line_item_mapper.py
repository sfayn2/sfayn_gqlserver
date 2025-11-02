from dataclasses import asdict
from ddd.order_management.application import dtos
from ddd.order_management.domain import models, value_objects, enums

class LineItemMapper:

    @staticmethod
    def to_domain(dto: dtos.ProductSkusDTO) -> models.LineItem:
        return models.LineItem(**dto.model_dump())
