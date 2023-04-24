from django.db import models
from django.contrib.auth.models import User
from utils.utils import path_and_rename


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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2category")
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
    goods_brand = models.CharField(max_length=30, null=True, blank=True)
    goods_desc = models.TextField(null=True) 
    status = models.IntegerField(null=True, choices=Status.choices, default=0) 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2product")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.product_sn} - {self.title}"


class Variant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2variant")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name


class VariantItem(models.Model):

    class Status(models.IntegerChoices):
        INACTIVE = 0
        ACTIVE = 1

    id = models.AutoField(primary_key=True)
    product_variant = models.ForeignKey("product.Variant", on_delete=models.CASCADE, null=True, related_name="variant2item", blank=True) 
    product_sn = models.ForeignKey("product.Product", on_delete=models.CASCADE, null=True, related_name="product2variantitem") 
    sku = models.CharField(max_length=50)
    quantity = models.IntegerField(null=True, blank=True, help_text="allocated or reserved quantity")
    price = models.FloatField(null=True, blank=True, help_text="sale price, exclusive of tax")
    options = models.CharField(max_length=50, null=True, blank=True) # Red/Blue?
    img_upload = models.ImageField(upload_to=path_and_rename, null=True, blank=True, help_text="Primary img")
    img_url = models.CharField(max_length=300, null=True, blank=True, help_text="secondary img") 
    default = models.BooleanField(default=False, help_text="default to display in product details page of similar product")
    status = models.IntegerField(null=True, choices=Status.choices, default=0) 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2variantsitem")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.product_sn} - {self.product_sn.title} ({self.product_variant}: {self.options})"




