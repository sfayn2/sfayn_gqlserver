import ast
from ddd.order_management.domain import value_objects, models, enums

class OfferStrategyMapper:

    @staticmethod
    def to_domain(django_filter_results) -> value_objects.OfferStrategy:
        #first coupon is invalid and second is valid should not stop processing Offer, hence, skipping error
        coupons = []
        for item in django_filter_results.get("coupons"):
            try:
                item.pop("id")
                coupons.append(value_objects.Coupon(**item))
            except:
                #TODO: add logger
                continue
        
        conditions = django_filter_results.get("conditions")

        return value_objects.OfferStrategy(
            conditions=ast.literal_eval(conditions),
            coupons=coupons,
            offer_type=enums.OfferType(django_filter_results.get("offer_type")),
            name=django_filter_results.get("name"),
            discount_value=django_filter_results.get("discount_value"),
            required_coupon=django_filter_results.get("required_coupon"),
            stackable=django_filter_results.get("stackable"),
            priority=django_filter_results.get("priority"),
            start_date=django_filter_results.get("start_date"),
            end_date=django_filter_results.get("end_date"),
            is_active=django_filter_results.get("is_active")
        )
