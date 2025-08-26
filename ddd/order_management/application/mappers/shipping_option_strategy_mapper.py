from dataclasses import asdict
from ddd.order_management.application import dtos
from ddd.order_management.domain import models, value_objects, enums

class ShippingOptionStrategyMapper:

    @staticmethod
    def to_domain(dto) -> value_objects.ShippingOptionStrategy:
        return value_objects.ShippingOptionStrategy(
            option_name=dto.option_name,
            method=dto.method,
            delivery_time=dto.delivery_time,
            conditions=json.loads(dto.conditions),
            base_cost=value_objects.Money(
                amount=dto.base_cost,
                currency=dto.currency
            ),
            flat_rate=value_objects.Money(
                amount=dto.flat_rate,
                currency=dto.currency
            ),
            #is_active=dto.is_active
        )