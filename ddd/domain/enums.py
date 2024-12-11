from enum import Enum

class ProductCategory(Enum):
    ELECTRONICS = 'Electronics'
    CLOTHING = 'Clothing'
    FURNITURE = 'Furniture'

class ProductStatus(Enum):
    DRAFT = "Draft"
    PENDING_REVIEW = "Pending Review"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    DEACTIVATED = "Deactivated"