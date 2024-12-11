
from dataclasses import dataclass
from ... import abstract_domain_models
from ._address import DeliveryAddress
from .dimensions import Dimensions
from .weight import Weight


@dataclass(frozen=True)
class DeliveryAddress(abstract_domain_models.ValueObject):
    address:  str
    postal:  int
    country:  str
    region:  str

    def __post_init__(self):
        if self.address is None:
            raise "Invalid address value!"

        if self.postal is None:
            raise "Invalid postal value!"

        if self.country is None:
            raise "Invalid country value!"

        if self.region is None:
            raise "Invalid region value!"


@dataclass(unsafe_hash=True)
class DeliveryPackage(abstract_domain_models.Entity):
    _delivery_address: DeliveryAddress

    _line_item_id: int
    _line_item_sku: str
    _dimensions: Dimensions
    _weight: Weight

    def __post_init__(self):
        if not self._line_item_id:
            raise "Invalid line item id!"

        if not self._line_item_sku:
            raise "Invalid line item sku!"

    def get_price(self, delivery_type: int):
        for package_price in self.get_package_prices():
        if package_price.get("deliviery_type") == delivery_type:
            package_price.get("price")
        return 

