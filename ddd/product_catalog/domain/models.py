import uuid
from abc import ABC
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from ddd.product_catalog.domain.value_objects import Money
from ddd.product_catalog.domain import enums

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
    _id: uuid.uuid4
    _sku: str
    _name: Variant
    _options: str
    _price: Money
    _stock: int
    _default: bool
    _is_active: bool

    #TODO: should be separate ?
    _tags: List[Tag] = field(default_factory=list)

    def __post_init__(self):
        if self._id is None:
            raise "Invalid variant item id!"
        
        if self._sku is None:
            raise "Invalid sku!"

        if self._name is None:
            raise "Invalid option!"

        if self._options is None:
            raise "Invalid option!"

        if self._stock is None:
            raise "Invalid stock!"

    #TODO: tag has its own lifecyle?
    #def add_tag(self, tag):
    #    if tag in self._tags:
    #        raise ValueError(f"Tag {tag} already exists")
    #    self._tags.append(tag)

    #def remove_tag(self, tag):
    #    if tag not in self._tags:
    #        raise ValueError(f"Tag {tag} not found")
    #    self._tags.remove(tag)

    #def get_tags(self):
    #    return self._tags

    def get_id(self):
        return self._id

    def get_sku(self):
        return self._sku

    def get_name(self):
        return self._name

    def get_options(self):
        return self._options

    def get_price(self):
        return self._price

    def get_stock(self):
        return self._stock

    def get_default(self):
        return self._default

    def is_active(self):
        return self._is_active


@dataclass
class Product:
    _id: uuid.uuid4
    _name: str
    _description: str
    _category: uuid.uuid4
    _created_by: str
    _status: enums.ProductStatus = enums.ProductStatus.DRAFT.name
    _variant_items: List[VariantItem] = field(default_factory=list)
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


    #def add_category(self, category: Category) -> None:
    #    if category not in self._categories:
    #        self._categories.append(category)

    #def remove_category(self, category_id: uuid.uuid4) -> None:
    #    self._categories = [c for c in self._categories if c.id != category_id]

    #def get_categories(self):
    #    return self._categories

    def update_modified_date(self):
        self._date_modified = datetime.now()

    def update_details(self, name: str, description: str) -> None:
        if not self.name:
            raise ValueError("Product name cannot be empty")
        self._name = name
        self._description = description
        self.update_modified_date()
    
    def update_status(self, new_status: enums.ProductStatus):
        if new_status not in self.VALID_STATUS_TRANSITIONS[self._status]:
            raise InvalidStatusTransitionError(f"Cannot transition from {self._status} to {new_status}")
        self._status = new_status
        self.update_modified_date()

    def activate(self) -> None:
        self.update_status(enums.ProductStatus.APPROVED.name)

    def deactivate(self) -> None:
        self.update_status(enums.ProductStatus.DEACTIVATED.name)

    def reject(self) -> None:
        self.update_status(enums.ProductStatus.REJECTED.name)

    def pending_review(self) -> None:
        self.update_status(enums.ProductStatus.PENDING_REVIEW.name)

    def add_variant_items(self, variant_item: VariantItem) -> None:
        if not variant_item:
            raise "No variant item to add in product catalog!"

        if variant_item not in self._variant_items:
            self._variant_items.append(variant_item)

    def remove_variant_items(self, variant_id: uuid.uuid4) -> None:
        self._variant_items = [v for v in self.variants if v.id != variant_id]
    
    def get_variant_items(self):
        return self._variant_items

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_desc(self):
        return self._description

    def get_status(self):
        return self._status

    def get_created_by(self):
        return self._created_by

    def get_date_created(self):
        return self._date_created

    def get_date_modified(self):
        return self._date_modified

    def get_category(self):
        return self._category
