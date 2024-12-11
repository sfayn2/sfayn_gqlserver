import uuid
from abc import ABC
from dataclasses import dataclass, field
from domain.value_objects import Money
from typing import List, Optional
from domain import enums

@dataclass
class Category:
    id: uuid.uuid4
    name: str
    parent: Optional['Category'] = None

@dataclass(frozen=True)
class VariantItem:
    id: uuid.uuid4
    option: str
    value: str
    price: Money
    stock: int

@dataclass
class ProductVariant:
    id: uuid.uuid4
    product_id: uuid.uuid4
    name: str
    items: List[VariantItem] = field(default_factory=list)


@dataclass
class ProductCatalog:
    id: uuid.uuid4
    name: str
    description: str
    status: enums.ProductStatus = enums.ProductStatus.DRAFT
    variants: List[ProductVariant] = field(default_factory=list)
    categories: List[Category]

    def add_variant(self, variant: ProductVariant) -> None:
        self.variants.append(variant)

    def remove_variant(self, variant_id: uuid.uuid4) -> None:
        self.variants = [v for v in self.variants if v.id != variant_id]

    def add_category(self, category: Category) -> None:
        if category not in self.categories:
            self.categories.append(category)

    def remove_category(self, category_id: uuid.uuid4) -> None:
        self.categories = [c for c in self.categories if c.id != category_id]

    def change_status(self, new_status: enums.ProductStatus):
        """ change the status of the product """
        if new_status not in enums.ProductStatus:
            raise ValueError(f"Invalid status: {new_status}")
        self.status = new_status

    def activate(self) -> None:
        if not self.status == enums.ProductStatus.PENDING_REVIEW:
            raise ValueError("Product must be in {enums.ProductStatus.PENDING_REVIEW}")
        self.change_status(enums.ProductStatus.APPROVED)

    def deactivate(self) -> None:
        if not self.status == enums.ProductStatus.APPROVED:
            raise ValueError("Product must be in {enums.ProductStatus.APPROVED}")
        self.change_status(enums.ProductStatus.APPROVED)

    def reject(self) -> None:
        if not self.status == enums.ProductStatus.PENDING_REVIEW:
            raise ValueError("Product must be in {enums.ProductStatus.PENDING_REVIEW}")
        self.change_status(enums.ProductStatus.REJECTED)

    def pending_review(self) -> None:
        if not self.status == enums.ProductStatus.DRAFT:
            raise ValueError("Product must be in {enums.ProductStatus.DRAFT}")
        self.change_status(enums.ProductStatus.DRAFT)

    