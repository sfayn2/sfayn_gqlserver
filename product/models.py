from django.db import models
from utils import path_and_rename
from decimal import Decimal
from django.conf import settings


# Create your models here.
class Category(models.Model):

    class LevelChoices(models.IntegerChoices):
        LEVEL_1 = 1
        LEVEL_2 = 2
        LEVEL_3 = 3

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    level = models.IntegerField(null=True, choices=LevelChoices.choices) 
    img_upload = models.ImageField(upload_to=path_and_rename, null=True, blank=True, help_text="Primary img")
    img_url = models.CharField(max_length=300, null=True, blank=True, help_text="secondary img") #TODO imagefield
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="user2category")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        if self.parent:
            return f"{self.name} - {self.parent} (level: {self.level})"
        else:
            return f"{self.name} (level: {self.level})"


class Product(models.Model):

    class Status(models.IntegerChoices):
        PENDING_REVIEW = 0
        APPROVED = 1
        REJECTED = 2

    #we can add more attributes later
    id = models.AutoField(primary_key=True)
    product_sn = models.CharField(max_length=50) #CharField to accept multiple sku datatype 
    title = models.CharField(max_length=100, null=True) 
    category = models.ForeignKey("product.Category", on_delete=models.CASCADE, null=True, related_name="cat2product") 
    goods_desc = models.TextField(null=True) 
    status = models.IntegerField(null=True, choices=Status.choices, default=0) 
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="user2product")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.product_sn} - {self.title}"


class Variant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="user2variant")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name


class VariantItem(models.Model):
    id = models.AutoField(primary_key=True)
    sku = models.CharField(max_length=50)
    product_variant = models.ForeignKey("product.Variant", on_delete=models.CASCADE, null=True, related_name="variant2item", blank=True) 
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, null=True, related_name="product2variantitem") 
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
    img_url = models.CharField(max_length=300, null=True, blank=True, help_text="secondary img") 

    default = models.BooleanField(default=False, help_text="default to display in product details page of similar product")
    is_active = models.BooleanField(default=False)
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="user2variantsitem")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.product.product_id} - {self.product.title} ({self.product_variant}: {self.options})"


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    img_upload = models.ImageField(upload_to=path_and_rename, null=True, blank=True, help_text="Primary img")
    img_url = models.CharField(max_length=300, null=True, blank=True, help_text="secondary img") 
    product_variant = models.ManyToManyField("product.VariantItem", related_name="prodvariant2tag", blank=True) 
    #how about category?
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="user2tags")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name


