from ddd.order_management.application import dtos
from ddd.order_management.domain import models
from ddd.order_management.application.mappers.vendor_details_mapper import VendorDetailsMapper
from ddd.order_management.application.mappers.package_mapper import PackageMapper
from ddd.order_management.application.mappers.money_mapper import MoneyMapper

class LineItemMapper:
    @staticmethod
    def to_domain(line_item_dto: dtos.LineItemDTO) -> models.LineItem:
        return models.LineItem(
            product_sku=line_item_dto.product_sku,
            product_name=line_item_dto.product_name,
            vendor=VendorDetailsMapper.to_domain(line_item_dto.vendor),
            product_category=line_item_dto.product_category,
            options=line_item_dto.options,
            product_price=MoneyMapper.to_domain(line_item_dto.product_price),
            order_quantity=line_item_dto.order_quantity,
            package=PackageMapper.to_domain(line_item_dto.package),
            is_free_gift=line_item_dto.is_free_gift,
            is_taxable=line_item_dto.is_taxable
        )