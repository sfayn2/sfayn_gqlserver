import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from decimal import Decimal
from ddd.product_catalog.domain import enums, models as domain_models, value_objects

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
    level = models.CharField(choices=enums.CategoryLevel.choices, max_length=15) 
    vendor = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="vendor2category", help_text="Vendor name associated w this category")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    class Meta:
        unique_together = ("name", "vendor") #prevent duplicate category per vendor

    def __str__(self):
        return f"{self.name} (Vendor name: {self.vendor.name})"

    def to_domain(self):
        category = domain_models.Category(
            _id=self.id,
            _name=self.name,
            _level=self.level,
            _parent_id=self.parent,
            _vendor_name=self.vendor_name,
            _date_created=self.date_created,
            _date_modified=self.date_modified
        ) 
        
        return category 

    @staticmethod
    def from_domain(category):
        category_model = Category.objects.update_or_create(
            id=category.get_id(), 
            defaults={ 
                "name":category.get_name(),
                "level":category.get_level(),
                "parent_id":category.get_parent_id(),
                "vendor_name":category.get_vendor_name(),
                "date_created": category.get_date_created(),
                "date_modified":category.get_date_modified()
            }
        )


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #uuid for global unique id
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True) 
    category = models.ManyToManyField("product_catalog.Category", blank=True, related_name="cat2product") 
    tag = models.ManyToManyField("product_catalog.Tag", related_name="tag2product", blank=True) 
    status = models.CharField(max_length=25, blank=True, null=True, choices=enums.ProductStatus.choices, default=enums.ProductStatus.DRAFT) 
    vendor = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="vendor2product", help_text="Vendor name associated w this product")
    brand = models.CharField(max_length=100, null=True, blank=True)
    package_weight = models.CharField(max_length=100, null=True, blank=True, help_text="value can be estimated package weight or based on historic data?")
    package_length = models.CharField(max_length=100, null=True, blank=True, help_text="value can be estimated package weight or based on historic data?")
    package_width = models.CharField(max_length=100, null=True, blank=True, help_text="value can be estimated package weight or based on historic data?")
    package_height = models.CharField(max_length=100, null=True, blank=True, help_text="value can be estimated package weight or based on historic data?")
    attributes = models.JSONField(blank=True, null=True, help_text='ex. {"other": "X", "Warranty": "1 year"}') # anticipated to have frequent changes on attributes, decided to use JSONField
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    class Meta:
        unique_together = ("name", "vendor") #prevent duplicate product per vendor

        #TODO: lets do this  in Vendor model?
        permissions = [
            ("vendor_standard_policy", "Can use vendor standard policy"),
            ("vendor_standard_v2_policy", "Can use vendor standard version2 policy"),
            ("vendor_standard_v3_policy", "Can use vendor standard version3 policy"),
        ]

    def __str__(self):
        return f"{self.name} (Vendor name: {self.vendor.name})"

    def to_domain(self):
        variants = [
            domain_models.VariantItem(
                _id=variant.id,
                _sku=variant.sku,
                _options=variant.options,
                _price=value_objects.Money(variant.price, "SGD"),
                _stock=value_objects.Stock(variant.stock),
                _default=variant.default,
                _is_active=variant.is_active,
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
            _vendor=self.vendor_id, 
            _date_created=self.date_created, 
            _date_modified=self.date_modified,
            _tags=list(self.tag.values_list('name', flat=True))
        ) 
        
        
        return product 

    @staticmethod
    def from_domain(product):
        product_model, created = Product.objects.update_or_create(
            id=product.get_id(), 
            defaults={ 
                "name": product.get_name(),
                "description": product.get_desc(),
                "category_id": product.get_category(),
                "status": product.get_status(),
                "vendor_id": product.get_vendor(),
                "date_created": product.get_date_created(),
                "date_modified": product.get_date_modified()
            }
        )

        product_model.tag.set(product.get_tags())

        for variant in product.get_variant_items():
            VariantItem.from_domain(variant, product_model.id)


class VariantItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #uuid for global unique id
    sku = models.CharField(max_length=50)
    product = models.ForeignKey("product_catalog.Product", on_delete=models.CASCADE, null=True, related_name="product2variantitem") 
    options = models.JSONField(help_text='ex. {"Size": "M", "Color": "RED"}') # anticipated to have complex tables to support multi dimension variants, decided to use JSONField
    price = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            help_text="default price, exclusive of tax", 
            default=Decimal("0.0")
        )
    stock = models.PositiveIntegerField()
    default = models.BooleanField(default=False, help_text="default to display in product details page of similar product")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name}  ({self.options})"

    @staticmethod
    def from_domain(variant, product_id):
        variant_model, created = VariantItem.objects.update_or_create(
            id=variant.get_id(),
            defaults={
                "sku": variant.get_sku(),
                "options": variant.get_options(),
                "price": variant.get_price(),
                "stock": variant.get_stock(),
                "default": variant.get_default(),
                "is_active": variant.is_active(),
                "product_id": product_id
            }

        )


        return variant_model

class Tag(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name

class Image(models.Model):
    variant = models.ForeignKey("product_catalog.VariantItem", on_delete=models.CASCADE, null=True, related_name="variant2images") 
    img_upload = models.ImageField(null=True, blank=True, help_text="variants img")
    order = models.PositiveIntegerField(default=1) # for ordering images

    def __str__(self):
        return f"{self.variant} {self.img_upload.url}"

