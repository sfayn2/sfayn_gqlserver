from django.db import models
from django.conf import settings
from decimal import Decimal

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name

class Offer(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="offers")
    name = models.CharField(max_length=255)
    offer_type = models.CharField(max_length=50)
    discount_value = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            help_text="Percentage or Fix amount?", 
            default=Decimal("0.0")
        )
    conditions = models.JSONField(help_text='ex. min_purchase, applicable_products')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

class ShippingOption(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="shipping_options")
    name = models.CharField(max_length=255)
    base_cost = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            help_text="", 
            default=Decimal("0.0")
        )

    #need this?
    conditions = models.JSONField(help_text='ex. only package under 30kg?')

    flat_rate = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            help_text="", 
            default=Decimal("0.0")
        )
    delivery_time = models.CharField(max_length=255)
