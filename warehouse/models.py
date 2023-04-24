from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Warehouse(models.Model):

    class Status(models.IntegerChoices):
        ACTIVE = 0
        IN_ACTIVE = 1

    name = models.CharField(max_length=20)
    address = models.TextField()
    postal = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    handling_fee = models.FloatField(null=True, blank=True, help_text="Add handling fee per order")
    status = models.IntegerField(null=True, choices=Status.choices) 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2warehouse")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.name} {self.address} {self.postal} {self.country}, {self.region}"


class Stock(models.Model):

    class Status(models.IntegerChoices):
        IN_STOCK = 0
        OUT_OF_STOCK = 1

    warehouse = models.ForeignKey('warehouse.Warehouse', on_delete=models.CASCADE, related_name="warehouse2stock")
    product_variant = models.ForeignKey('product.VariantItem', on_delete=models.CASCADE, related_name="product_variant2stock")
    stock = models.IntegerField(null=True, blank=True, help_text="warehouse stocks ")
    price = models.FloatField(null=True, blank=True, help_text="warehouse pricing")
    status = models.IntegerField(null=True, choices=Status.choices) 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2stock")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.warehouse} {self.stock} {self.price}"

