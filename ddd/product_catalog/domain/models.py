import uuid
from abc import ABC
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from ddd.product_catalog.domain.value_objects import Money, Stock
from ddd.product_catalog.domain import vendor_policies
from ddd.product_catalog.domain import enums, exceptions

class InvalidStatusTransitionError(Exception):
    pass

#Aggregate Root
@dataclass
class Category:
    _id: uuid.uuid4
    _name: str
    _level: enums.CategoryLevel
    _vendor_name: Optional[str] = None
    _parent_id: Optional[int] = None
    _subcategories: List[uuid.uuid4] = field(default_factory=list)
    _date_created: datetime = field(default_factory=datetime.now)
    _date_modified: Optional[datetime] = None

    def __post_init__(self):
        if self._level not in [c.name for c in enums.CategoryLevel]:
            raise ValueError(f"Invalid level: {self._level}")

        if self._parent_id is None and self._level != enums.CategoryLevel.LEVEL_1.name:
            raise ValueError(f"Only {enums.CategoryLevel.LEVEL_1.name} categories can have no parent.")

    def update_modified_date(self):
        self._date_modified = datetime.now()

    #TODO: to add back when really need?
    #def add_subcategory(self, subcategory_id: uuid.uuid4, subcategory_lvl: enums.CategoryLevel) -> None:
    #    #TODO: not clean using split?
    #    lvl_num = self._level.split("_")[1]
    #    subcat_lvl_num = subcategory_lvl.name.split("_")[1]
    #    if lvl_num + 1 != subcat_lvl_num:
    #        raise ValueError(f"Subcategory level must be ${lvl_num + 1}.")

    #    if subcategory_id in self._subcategories:
    #        raise ValueError(f"Subcategory {subcategory_id} already exists.")

    #    self._subcategories.append(subcategory_id)
    #    self.update_modified_date()

    #def remove_category(self, subcategory_id: uuid.uuid4) -> None:
    #    self._subcategories = [c for c in self._subcategories if c != subcategory_id]

    def rename(self, new_name: str):
        if not new_name.strip():
            raise ValueError("Category name cannot be empty.")
        self._name = new_name
        self.update_modified_date()

    def update_level(self, new_level: enums.CategoryLevel):
        if new_level not in [c.name for c in enums.CategoryLevel]:
            raise ValueError(f"Invalid level: {self._level}")
        self._level = new_level
        self.update_modified_date()

    def set_to_level_1(self):
        self.update_level("LEVEL_1")

    def set_to_level_2(self):
        self.update_level("LEVEL_2")
    
    def set_to_level_3(self):
        self.update_level("LEVEL_3")

    def get_id(self):
        return self._id

    def get_parent_id(self):
        return self._parent_id

    def get_name(self):
        return self._name

    def get_level(self):
        return self._level

    def get_vendor_name(self):
        return self._vendor_name

    def get_date_created(self):
        return self._date_created

    def get_date_modified(self):
        return self._date_modified


#@dataclass(frozen=True)
#class Tag:
#    name: str

@dataclass
class VariantItem:
    _id: uuid.uuid4
    _sku: str
    _options: str
    _price: Money
    _stock: Stock
    _default: bool
    _is_active: bool

    def __post_init__(self):
        if self._id is None:
            raise ValueError("Variant item id cannot be empty")
        
        if self._sku is None:
            raise ValueError("Variant item sku cannot be empty")

        #TODO: this accepts JSON now
        if self._options is None:
            raise ValueError("Variant item options cannot be empty")
    
    def deactivate(self):
        self._is_active = False

    def activate(self):
        self._is_active = True

    def get_id(self):
        return self._id

    def get_sku(self):
        return self._sku

    def get_options(self):
        return self._options

    def get_price(self):
        return self._price.get_amount()

    def get_stock(self):
        return self._stock.get_quantity()

    def get_default(self):
        return self._default

    def is_active(self):
        return self._is_active


#Aggregate Root
@dataclass
class Product:
    _id: uuid.uuid4
    _name: str
    _description: str
    _category: uuid.uuid4
    _vendor: int
    _tags: List[str] = field(default_factory=list)
    _status: enums.ProductStatus = enums.ProductStatus.DRAFT.name
    variants: List[VariantItem] = field(default_factory=list)
    _date_created: datetime = field(default_factory=datetime.now)
    _date_modified: Optional[datetime] = None

    VALID_STATUS_TRANSITIONS = {
        enums.ProductStatus.DRAFT.name : [enums.ProductStatus.PENDING_REVIEW.name],
        enums.ProductStatus.PENDING_REVIEW.name : [enums.ProductStatus.APPROVED.name, enums.ProductStatus.REJECTED.name],
        enums.ProductStatus.APPROVED.name : [enums.ProductStatus.DEACTIVATED.name],
        enums.ProductStatus.DEACTIVATED.name : [enums.ProductStatus.PENDING_REVIEW.name, enums.ProductStatus.DRAFT.name],
    }

    def update_category(self, category_id: uuid.uuid4):
        self._category = category_id
        self.update_modified_date()

    def update_modified_date(self):
        self._date_modified = datetime.now()

    def update_details(self, name: str, description: str) -> None:
        if not self.name:
            raise ValueError("Product name cannot be empty")
        self._name = name
        self._description = description
        self.update_modified_date()
    
    def change_state(self, new_status: enums.ProductStatus):
        if new_status not in self.VALID_STATUS_TRANSITIONS[self._status]:
            raise exceptions.InvalidStatusTransitionError(f"Cannot transition from {self._status} to {new_status}")
        self._status = new_status
        self.update_modified_date()

    def approve(self) -> None:
        self.change_state(enums.ProductStatus.APPROVED.name)

    def deactivate(self) -> None:
        self.change_state(enums.ProductStatus.DEACTIVATED.name)

    def reject(self) -> None:
        self.change_state(enums.ProductStatus.REJECTED.name)

    def pending_review(self) -> None:
        self.change_state(enums.ProductStatus.PENDING_REVIEW.name)

    def add_variants(self, variant_item: VariantItem) -> None:
        if not variant_item:
            raise "No variant item to add in product catalog!"

        if variant_item not in self.variants:
            self.variants.append(variant_item)

    def deactivate_sku(self, sku: str) -> None:
        for v in self.variants:
            if v.get_sku() == sku:
                v.deactivate()

    def activate_sku(self, sku: str) -> None:
        for v in self.variants:
            if v.get_sku() == sku:
                v.activate()

    def add_tag(self, tag: str):
        if tag in self._tags:
            raise ValueError(f"Tag {tag} already exists")
        self._tags.append(tag)

    def remove_tag(self, tag: str):
        if tag not in self._tags:
            raise ValueError(f"Tag {tag} not found")
        self._tags.remove(tag)

    def get_tags(self):
        return self._tags
    
    def get_variant_items(self):
        return self.variants

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_desc(self):
        return self._description

    def get_status(self):
        return self._status

    def get_vendor(self):
        return self._vendor

    def get_date_created(self):
        return self._date_created

    def get_date_modified(self):
        return self._date_modified

    def get_category(self):
        return self._category
