from django.db import models
from django.conf import settings
import uuid
from decimal import Decimal
from ddd.product_catalog.domain import enums, models as domain_models
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

    def to_domain(self):
        category = domain_models.Category(
            _id=self.id,
            _name=self.name,
            _level=self.level,
            _parent_id=self.parent,
            _created_by=self.created_by,
            _date_created=self.date_created,
            _date_modified=self.date_modified
        ) 
        
        return category 

    @staticmethod
    def from_domain(category):
        category_model = Category.objects.update_or_create(
            id=category.get_id(), 
            defaults={ 
                "id":category.id,
                "name":category.name,
                "level":category.level,
                "parent_id":category.parent,
                "created_by":category.created_by,
                "date_created": category.date_created,
                "date_modified":category.date_modified
            }
        )


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

    def to_domain(self):
        variants = [
            domain_models.VariantItem(
                _id=variant.id,
                _sku=variant.sku,
                _name=variant.name,
                _options=variant.options,
                _price=variant.price,
                _stock=variant.stock,
                _default=variant.default,
                _is_active=variant.is_active,
                _tags=list(variant.prodvariant2tag.values_list('name', flat=True))
            )
            for variant in self.product2variantitem.all()
        ]

        product = domain_models.Product(
            _id=self.id,
            _name=self.name,
            _description=self.description,
            _status=self.status,
            _variant_items=variants,
            _category=self.category.id,
            _created_by=self.created_by, 
            _date_created=self.date_created, 
            _date_modified=self.date_modified
        ) 
        
        
        return product 

    @staticmethod
    def from_domain(product):
        product_model = Product.objects.update_or_create(
            id=product.get_id(), 
            defaults={ 
                "name": product.get_name(),
                "description": product.get_desc(),
                "category_id": product.get_category(),
                "status": product.get_status(),
                "created_by": product.get_created_by(),
                "date_created": product.get_date_created(),
                "date_modified": product.get_date_modified()
            }
        )

        for variant in product.get_variant_items():
            VariantItem.from_domain(variant)


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

    @staticmethod
    def from_domain(variant):
        variant_model = VariantItem.objects.update_or_create(
            id=variant.get_id(),
            defaults={
                "sku": variant.get_sku(),
                "name": variant.get_name(),
                "options": variant.get_options(),
                "price": variant.get_price(),
                "stock": variant.get_stock(),
                "default": variant.get_default(),
                "is_active": variant.is_active(),
            }

        )

        return variant_model

class Tag(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    product_variant = models.ManyToManyField("product_catalog.VariantItem", related_name="prodvariant2tag", blank=True) 
    created_by = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name
