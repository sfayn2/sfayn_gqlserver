from django.db import models
from django.contrib.auth.models import User
from utils import path_and_rename
from django.conf import settings
from decimal import Decimal

# Create your models here.
# decided to move provider here to have a loosely coupled/ self contained warehouse module
class Provider(models.Model): 
    name = models.CharField(max_length=20) #can be outsource?
    address = models.TextField(blank=True, null=True)
    postal = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    thumbnail_url = models.ImageField(upload_to=path_and_rename, null=True, blank=True, help_text="thumbnail url")
    handling_fee = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            null=True, 
            blank=True, 
            help_text="Add handling fee ", 
        )
    is_active = models.BooleanField(default=False)
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="user2warehouse")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.name} ({self.company_url})"


class Stock(models.Model):

    class Status(models.IntegerChoices):
        IN_STOCK = 0
        OUT_OF_STOCK = 1
        LOW_STOCK = 2

    warehouse = models.ForeignKey('warehouse.Provider', on_delete=models.CASCADE, related_name="warehouse2stock")
    sku = models.CharField(max_length=50, blank=True, null=True, help_text="product variant stock keeping unit")
    #product_variant = models.ForeignKey('product.VariantItem', on_delete=models.CASCADE, related_name="prodvariant2stock")

    # stock can be updated using webhook? or directly do external http request ?
    stock = models.IntegerField(null=True, blank=True, help_text="warehouse stocks ")
    low_stock = models.IntegerField(null=True, blank=True, help_text="warehouse low stock to track inventory? ")
    price = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            null=True, 
            blank=True, 
            help_text="warehouse stock price", 
            default=Decimal("0.0")
        )
    status = models.IntegerField(null=True, choices=Status.choices) 
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="user2stock")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.warehouse} {self.stock} {self.price}"

