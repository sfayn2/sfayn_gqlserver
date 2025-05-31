import ast
from ddd.order_management.domain import value_objects, models

class ShippingOptionStrategyMapper:

    @staticmethod
    def to_domain(django_filter_results) -> value_objects.ShippingOptionStrategy:
        return value_objects.ShippingOptionStrategy(
            name=django_filter_results.get("name"),
            delivery_time=django_filter_results.get("delivery_time"),
            conditions=django_filter_results.get("conditions"),
            base_cost=value_objects.Money(django_filter_results.get("base_cost")),
            flat_rate=value_objects.Money(django_filter_results.get("flat_rate")),
            currency=django_filter_results.get("currency"),
            is_active=django_filter_results.get("is_active")
        )