
from dataclasses import dataclass
from ....delivery_domain import abstract_domain_models
from .delivery_address import DeliveryAddress
from .dimensions import Dimensions
from .weight import Weight

@dataclass(unsafe_hash=True)
class DeliveryPackage(abstract_domain_models.Entity):
    _delivery_address: DeliveryAddress 
    _delivery_pincode: int
    _delivery_type: int 
    _item_sku: str #TODO valueobject?
    _item_quantity: int = 1
    _dimensions: Dimensions
    _weight: Weight
    _contact_number: int
    _email: str
    _name: str


    def __post_init__(self):
        if self._item_quantity <= 0:
            raise "Invalid quantity!"


    def add_quantity(self, quantity: int):
        if quantity < 0:
            raise "Invalid quantity!"

        self._quantity += quantity

    def get_item_quantity(self):
        return self._item_quantity

    def get_item_sku(self):
        return self._item_sku
