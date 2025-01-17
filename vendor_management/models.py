from django.db import models
from django.conf import settings
from decimal import Decimal

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    is_active = models.BooleanField(default=True, help_text="To quickly control whether the is valid")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name

class Coupon(models.Model):
    coupon_code = models.CharField(max_length=50, help_text="e.g WELCOME25")
    start_date = models.DateTimeField(help_text="Only valid on start of this date")
    end_date = models.DateTimeField(help_text="Only valid on before end date")
    is_active = models.BooleanField(default=False, help_text="To quickly control whether this offer is still valid")

    def __str__(self):
        return self.coupon_code

class Offer(models.Model):
    OFFER_TYPE_CHOICES = (
        ('percentage_discount', 'Percentage Discount'),
        ('fixed_discount', 'Fixed Discount'),
        ('coupon_discount', 'Coupon Percentage Discount'),
        ('bundle', 'Bundle'),
        ('free_gift', 'Free Gift'),
        ('free_shipping', 'Free Shipping'),
    )
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="offers")
    name = models.CharField(max_length=255)
    offer_type = models.CharField(max_length=50, choices=OFFER_TYPE_CHOICES)
    discount_value = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            help_text="Percentage or Fix amount?", 
            default=Decimal("0.0")
        )
    conditions = models.JSONField(help_text='ex. min_purchase, applicable_products')
    stackable = models.BooleanField(default=False, help_text="Set to True, To combine w other stackable")
    priority = models.PositiveIntegerField(default=0, help_text="The highest number will be prioritized on multistack or single stack")
    required_coupons = models.BooleanField(default=False, help_text="Set to True, To make use of coupons to apply")
    coupon = models.ManyToManyField(Coupon, blank=True, null=True, help_text="Provide a coupons to manually apply for this offer.")
    start_date = models.DateTimeField(help_text="Only valid on start of this date; To ignore if required_coupon is True", blank=True, null=True)
    end_date = models.DateTimeField(help_text="Only valid on before end date; To ignore if required_coupon is True", blank=True, null=True)
    #manual_apply = models.BooleanField(default=False, help_text="Determine whether to apply manually.; To ignore if required_coupons")
    is_active = models.BooleanField(default=False, help_text="To quickly control whether this offer is still valid")


    def __str__(self):
        return f"{self.name} ( {self.offer_type} )"



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

    def __str__(self):
        return f"{self.name} ( {self.delivery_time} )"
