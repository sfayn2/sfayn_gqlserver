import ast
from typing import List
from dataclasses import asdict
from ddd.order_management.application import dtos
from ddd.order_management.domain import value_objects
from ddd.order_management.application.mappers.shipping_details_mapper import ShippingDetailsMapper

class ShippingOptionsResponseMapper:

    @staticmethod
    def to_dtos(shipping_options: List[value_objects.ShippingDetails]) -> List[dtos.ShippingDetailsDTO]:
        return [ShippingDetailsMapper.to_dto(option) for option in shipping_options]