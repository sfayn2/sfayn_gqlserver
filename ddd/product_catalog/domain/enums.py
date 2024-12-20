from enum import Enum

class ProductCategory(Enum):
    ELECTRONICS = 'Electronics'
    CLOTHING = 'Clothing'
    FURNITURE = 'Furniture'


class ProductStatus(Enum):
    DRAFT = "Draft"
    PUBLISHED = "Published"
    PENDING_REVIEW = "Pending Review"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    DEACTIVATED = "Deactivated"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class CategoryLevel(Enum):
    LEVEL_1 = "Level 1"
    LEVEL_2 = "Level 2"
    LEVEL_3 = "Level 3"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)