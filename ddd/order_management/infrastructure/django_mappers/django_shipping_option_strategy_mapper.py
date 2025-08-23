import ast, json
from ddd.order_management.domain import value_objects, models, enums

#TODO to cleanup
class ShippingOptionStrategyMapper:

    @staticmethod
    def to_domain(django_filter_results) -> value_objects.ShippingOptionStrategy:
        return value_objects.ShippingOptionStrategy(
            option_name=django_filter.get("option_name"),
            method=enums.ShippingMethod(django_filter_results.get("method")),
            provider=django_filter_results.get("provider"),
            delivery_time=django_filter_results.get("delivery_time"),
            conditions=json.loads(django_filter_results.get("conditions")),
            base_cost=value_objects.Money(
                amount=django_filter_results.get("base_cost"),
                currency=django_filter_results.get("currency")
            ),
            flat_rate=value_objects.Money(
                amount=django_filter_results.get("flat_rate"),
                currency=django_filter_results.get("currency")
            ),
            is_active=django_filter_results.get("is_active")
        )