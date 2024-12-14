from django.db import models
from django.conf import settings
import uuid
from decimal import Decimal
from ddd.product_catalog.domain import enums
from utils import path_and_rename

# Create your models here.
class Category(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #uuid for global unique id
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self', 
        blank=True, 
        null=True, 
        on_delete=models.CASCADE, 
        related_name="subcategories"
    )
    level = models.CharField(blank=True, null=True, choices=enums.CategoryLevel.choices, max_length=15) 
    created_by = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        if self.parent:
            return f"{self.name} - {self.parent} (level: {self.level})"
        else:
            return f"{self.name} (level: {self.level})"

class Product(models.Model):

    #we can add more attributes later
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #uuid for global unique id
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True) 
    category = models.ForeignKey("product_catalog.Category", on_delete=models.CASCADE, null=True, related_name="cat2product") 
    status = models.CharField(max_length=25, blank=True, null=True, choices=enums.ProductStatus.choices, default=enums.ProductStatus.DRAFT) 
    created_by = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name

class VariantItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #uuid for global unique id
    sku = models.CharField(max_length=50)
    product = models.ForeignKey("product_catalog.Product", on_delete=models.CASCADE, null=True, related_name="product2variantitem") 
    name = models.CharField(max_length=100, blank=True, null=True)
    options = models.CharField(max_length=50, null=True, blank=True) # Red/Blue?
    price = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            null=True, 
            blank=True, 
            help_text="default price, exclusive of tax", 
            default=Decimal("0.0")
        )
    stock = models.PositiveIntegerField()
    img_upload = models.ImageField(upload_to=path_and_rename, null=True, blank=True, help_text="Primary img")
    default = models.BooleanField(default=False, help_text="default to display in product details page of similar product")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name}  ({self.name}: {self.options})"

class Tag(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    product_variant = models.ManyToManyField("product_catalog.VariantItem", related_name="prodvariant2tag", blank=True) 
    created_by = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name
