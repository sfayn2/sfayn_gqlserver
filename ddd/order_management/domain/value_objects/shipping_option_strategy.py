from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from ddd.order_management.domain import enums, exceptions
from .money import Money

@dataclass(frozen=True) 
class ShippingOptionStrategy:

    #for UI display, e.g. MyStandard
    option_name: str 
    delivery_time: str

    method: enums.ShippingMethod
    conditions: dict
    base_cost: Money
    flat_rate: Money
    is_active: bool
    #currency: str

    def __post_init__(self):
        if not isinstance(self.method, enums.ShippingMethod):
            raise exceptions.ShippingOptionStrategyException("Invalid shipping method name")

        if not isinstance(self.display_name, str) or not self.display_name.strip():
            raise exceptions.ShippingOptionStrategyException("Display name must be a valid non-empty string. e.g. (2-3 Days delivery)")

        if not isinstance(self.delivery_time, str) or not self.delivery_time.strip():
            raise exceptions.ShippingOptionStrategyException("Delivery time must be a valid non-empty string. e.g. (2-3 Days delivery)")

        if self.method in (enums.ShippingMethod.STANDARD, enums.ShippingMethod.EXPRESS):
            if not isinstance(self.conditions.get("max_weight"), (Decimal, int)):
                raise exceptions.ShippingOptionStrategyException("Standard/Express shipping must specify a max_weight. ie {'max_weight': 30}")
        if self.method == enums.ShippingMethod.EXPRESS:
            if not self._is_valid_time_format(self.conditions.get("cutoff_time")):
                raise exceptions.ShippingOptionStrategyException("Express shipping must specify a valid cutoff time in HH:MM format. (e.g. {'cutoff_time': '14:00'})")
        if self.method == enums.ShippingMethod.LOCAL_PICKUP:
            pickup_time_from = self.conditions.get("pickup_time_from")
            pickup_time_to = self.conditions.get("pickup_time_to")
            if not self.conditions.get("near_by_cities"):
                raise exceptions.ShippingOptionStrategyException("Local Pickup must specify a near by cities. (e.g. {'near_by_cities': ['city1', 'city2']})")
            if not (self._is_valid_time_format(pickup_time_from) and self._is_valid_time_format(pickup_time_to)):
                raise exceptions.ShippingOptionStrategyException("Local Pickup must specify a valid pickup times. (e.g. { 'pickup_time_from': '14:00', 'pickup_time_to': '15:00' } )")
        if self.method == enums.ShippingMethod.FREE_SHIPPING:
            min_order_amount = self.conditions.get("min_order_amount")
            if not isinstance(min_order_amount, Decimal) or min_order_amount < Decimal("0"):
                raise exceptions.ShippingOptionStrategyException("Free Shipping must speicify a valid minimum order amount (e.g. { 'min_order_amount': Decimal('50') })")

        if self.method == enums.ShippingMethod.OTHER:
            if not self.conditions.get("carrier_name"):
                raise exceptions.ShippingOptionStrategyException("Other shipping must specify carrier name. (e.g. {'carrier_name': 'Fedex', 'service_code': 'FEDEX_GROUND'})")

    def _is_valid_time_format(self, time: str) -> bool:
        try:
            datetime.strptime(time, "%H:%M")
            return True
        except exceptions.ShippingOptionStrategyException:
            return False



