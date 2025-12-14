from dataclasses import asdict
from ddd.order_management.application import dtos
from ddd.order_management.domain import models, value_objects, enums

class LineItemMapper:

    @staticmethod
    def to_domain(dto: dtos.ProductSkusRequestDTO) -> models.LineItem:
        return models.LineItem(
            product_sku=dto.product_sku,
            product_name=dto.product_name,
            order_quantity=dto.order_quantity,
            vendor_id=dto.vendor_id,
            package=value_objects.Package(dto.package.weight_kg),
            product_price=value_objects.Money(amount=dto.product_price.amount, currency=dto.product_price.currency),
        )

    @staticmethod
    def to_response_dto(line_item: models.LineItem) -> dtos.LineItemResponseDTO:
        return dtos.LineItemResponseDTO(**asdict(line_item))
