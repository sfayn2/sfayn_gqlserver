import uuid
from abc import ABC
from dataclasses import dataclass, field
from ddd.domain.value_objects import Money
from typing import List, Optional
from ddd.domain import enums

class InvalidStatusTransitionError(Exception):
    pass


@dataclass
class Category:
    _category_id: uuid.uuid4
    _name: str
    _parent: Optional['Category'] = None

    def set_name(self, new_name: str):
        if self._name is None:
            raise "Invalid category name!"
        self._name = new_name

    def get_name(self):
        return self._name

@dataclass(frozen=True)
class Variant:
    name: str

@dataclass(frozen=True)
class Tag:
    name: str

@dataclass
class VariantItem:
    _variant_item_id: uuid.uuid4
    _product_variant: Variant
    _option: str
    _value: str
    _price: Money
    _stock: int
    _tags: List[Tag] = field(default_factory=list)

    def __post_init__(self):
        if self._variant_item_id is None:
            raise "Invalid variant item id!"

        if self._option is None:
            raise "Invalid option!"

        if self._value is None:
            raise "Invalid value!"

        if self._stock is None:
            raise "Invalid stock!"

    def add_tag(self, tag):
        if tag in self._tags:
            raise ValueError(f"Tag {tag} already exists")
        self._tags.append(tag)

    def remove_tag(self, tag):
        if tag not in self._tags:
            raise ValueError(f"Tag {tag} not found")
        self._tags.remove(tag)

    def get_tags(self):
        return self._tags



@dataclass
class ProductCatalog:
    _id: uuid.uuid4
    _name: str
    _description: str
    _status: enums.ProductStatus = enums.ProductStatus.DRAFT
    _variant_items: List[VariantItem] = field(default_factory=list)
    _categories: List[Category] = field(default_factory=list)

    VALID_STATUS_TRANSITIONS = {
        enums.ProductStatus.DRAFT : [enums.ProductStatus.PENDING_REVIEW],
        enums.ProductStatus.PENDING_REVIEW : [enums.ProductStatus.APPROVED, enums.ProductStatus.REJECTED],
        enums.ProductStatus.APPROVED : [enums.ProductStatus.DEACTIVATED],
    }

    def add_category(self, category: Category) -> None:
        if category not in self._categories:
            self._categories.append(category)

    def remove_category(self, category_id: uuid.uuid4) -> None:
        self._categories = [c for c in self._categories if c.id != category_id]

    def get_categories(self):
        return self._categories

    def update_details(self, name: str, description: str) -> None:
        if not self.name:
            raise ValueError("Product name cannot be empty")
        self._name = name
        self._description = description
    
    def update_status(self, new_status: enums.ProductStatus):
        if new_status not in self.VALID_STATUS_TRANSITIONS[self._status]:
            raise InvalidStatusTransitionError(f"Cannot transition from {self._status} to {new_status}")
        self._status = new_status

    def get_product_status(self):
        return self._status

    def activate(self) -> None:
        self.update_status(enums.ProductStatus.APPROVED)

    def deactivate(self) -> None:
        self.update_status(enums.ProductStatus.DEACTIVATED)

    def reject(self) -> None:
        self.update_status(enums.ProductStatus.REJECTED)

    def pending_review(self) -> None:
        self.update_status(enums.ProductStatus.PENDING_REVIEW)

    def add_variant_items(self, variant_item: VariantItem) -> None:
        if not variant_item:
            raise "No variant item to add in product catalog!"

        if variant_item not in self._variant_items:
            self._variant_items.append(variant_item)

    def remove_variant_items(self, variant_id: uuid.uuid4) -> None:
        self._variant_items = [v for v in self.variants if v.id != variant_id]
    
    def get_variant_items(self):
        return self._variant_items