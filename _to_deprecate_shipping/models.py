from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from decimal import Decimal
from utils import path_and_rename

# Create your models here.
class Zone(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, help_text="ex. Zone 1")
    country = models.CharField(max_length=50, help_text="ex. Singapore")
    region = models.CharField(max_length=50, help_text="ex. Tampines")
    created_by = models.ForeignKey(
        User, 
        null=True,
        blank=True,
        on_delete=models.CASCADE, 
        related_name="user2zone"
    )
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f'{self.name} {self.country}, {self.region}'




class Carrier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20) #can be outsource?
    tracker_url = models.CharField(max_length=200, blank=True, null=True)
    logo = models.ImageField(upload_to=path_and_rename, null=True, blank=True, help_text="company logo")
    is_active = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2provider")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.name}"



class Method(models.Model):
    id = models.AutoField(primary_key=True)
    #tax 1 to many?
    name = models.CharField(max_length=50, help_text="ex. Free shipping, Local pickup")
    desc = models.CharField(max_length=150, blank=True, null=True)

    # offer shipping method on the same zone
    shipping_zone = models.ManyToManyField('shipping.Zone', related_name="zone2method", blank=True)

    # offer shipping method only on the selected vendor?
    vendor = models.ManyToManyField('accounts.Vendor', blank=True, related_name="vendor2method")

    # offer shipping method only on the same tag?
    tag = models.ManyToManyField('product.Tag', blank=True, related_name="tag2method")

    # offer shipping method only on the selected items?
    product_variant = models.ManyToManyField('product.VariantItem', blank=True, related_name="prodvariant2method")

    # offer shipping method only on the selected category?
    category = models.ManyToManyField('product.Category', blank=True, related_name="category2method")

    #get the shipping cost based on classification
    rates = models.TextField(
            help_text="ex. [{ 'name': '3 hours express', 'max_Weight_kg': 1, min_LWH_cm: 60, 'cost':  14 }, { 'name': 'Specific Delivery Slot', 'max_Weight_kg': 1, min_LWH_cm: 60, 'cost':  18 }, ]",
            blank=True,
            null=True
        )

    #get the shipping cost based on provider calculate rate
    #fulfillment provider or carrier?
    carrier = models.ForeignKey(
        'shipping.Carrier', 
        null=True,
        blank=True,
        on_delete=models.CASCADE, 
        related_name="carrier2method"
    )

    is_enable = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, 
        null=True,
        blank=True,
        on_delete=models.CASCADE, 
        related_name="user2method"
    )
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f'{self.title} {self.desc}, {self.cost}'




