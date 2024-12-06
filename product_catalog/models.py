from django.db import models
from decimal import Decimal
from django.conf import settings
import uuid
from utils import path_and_rename

# Create your models here.
class Category(models.Model):

    class LevelChoices(models.TextChoices):
        LEVEL_1 = "level_1", "Level 1"
        LEVEL_2 = "level_2", "Level 2"
        LEVEL_3 = "level_3", "Level 3"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #uuid for global unique id
    name = models.CharField(max_length=100)
    img_upload = models.ImageField(upload_to=path_and_rename, null=True, blank=True, help_text="Primary img")
    parent = models.ForeignKey(
        'self', 
        blank=True, 
        null=True, 
        on_delete=models.CASCADE, 
        related_name="subcategories"
    )
    level = models.CharField(blank=True, null=True, choices=LevelChoices, max_length=15) 
    created_by = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        if self.parent:
            return f"{self.name} - {self.parent} (level: {self.level})"
        else:
            return f"{self.name} (level: {self.level})"

class Product(models.Model):

    class ProductStatus(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING = "pending_review", "Pending Review"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        DEACTIVATED = "deactivated", "Deactivated"

    #we can add more attributes later
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #uuid for global unique id
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True) 
    category = models.ForeignKey("product_catalog.Category", on_delete=models.CASCADE, null=True, related_name="cat2product") 
    status = models.CharField(max_length=25, blank=True, null=True, choices=ProductStatus, default=ProductStatus.DRAFT) 
    created_by = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name

class Variant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #uuid for global unique id
    name = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name

class VariantItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #uuid for global unique id
    sku = models.CharField(max_length=50)
    product = models.ForeignKey("product_catalog.Product", on_delete=models.CASCADE, null=True, related_name="product2variantitem") 
    product_variant = models.ForeignKey("product_catalog.Variant", on_delete=models.CASCADE, null=True, related_name="variant2item", blank=True) 
    price = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            null=True, 
            blank=True, 
            help_text="sale price, exclusive of tax", 
            default=Decimal("0.0")
        )
    options = models.CharField(max_length=50, null=True, blank=True) # Red/Blue?
    img_upload = models.ImageField(upload_to=path_and_rename, null=True, blank=True, help_text="Primary img")
    default = models.BooleanField(default=False, help_text="default to display in product details page of similar product")
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.product.name}  ({self.product_variant}: {self.options})"

class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #uuid for global unique id
    name = models.CharField(max_length=100, blank=True, null=True)
    product_variant = models.ManyToManyField("product_catalog.VariantItem", related_name="prodvariant2tag", blank=True) 
    created_by = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name
