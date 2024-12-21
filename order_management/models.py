from django.db import models
from django.conf import settings

# Create your models here.

class Order(models.Model):
    order_id = models.CharField(max_length=255, primary_key=True)

    order_status = models.CharField(
        max_length=25, 
        blank=True, 
        null=True, 
        choices=(), 
        default="PENDING"
    ) 

    shipping_method = models.CharField(max_length=50, null=True, blank=True, help_text="i.e. Free Shipping, Local Pickup")
    shipping_note = models.CharField(max_length=150, null=True, blank=True, help_text="i.e. 2-3 days delivery")
    shipping_cost = models.DecimalField(
        decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
        max_digits=settings.DEFAULT_MAX_DIGITS,
        null=True, 
        blank=True, 
        help_text="", 
    )

    shipping_address = models.TextField(blank=True, help_text="Delivery address")
    shipping_postal = models.CharField(max_length=50)
    shipping_country = models.CharField(max_length=50)
    shipping_region = models.CharField(max_length=50)

    total_amount = models.DecimalField(
        decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
        max_digits=settings.DEFAULT_MAX_DIGITS,
        null=True, 
        blank=True, 
        help_text="", 
    )
    created_by = models.CharField(
        max_length=50, 
        null=True, 
        blank=True, 
        help_text="always system user?")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.order_id} - {self.shipping_address} ( {self.status} )"


class OrderLine(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(
        "order.Order", 
        on_delete=models.CASCADE,
        related_name="order2orderitem", 
        null=True, 
        blank=True
    )

    product_sku = models.CharField(max_length=50)
    product_variant = models.CharField(max_length=50, null=True, blank=True) # COLOR?
    product_option = models.CharField(max_length=50, null=True, blank=True) # Red/Blue?
    product_img = models.ImageField(null=True, blank=True, help_text="Primary img")
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_quantity = models.PositiveIntegerField(null=True)
    total_price = models.DecimalField(
        decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
        max_digits=settings.DEFAULT_MAX_DIGITS,
        null=True, 
        blank=True, 
        help_text="", 
    )


    def __str__(self):
        return f"Item {self.product_variant} ({self.quantity})"

class Shipping(models.Model):
    order = models.OneToOneField(Order, related_name="shipping", on_delete=models.CASCADE)
    provider_name = models.CharField(max_length=255, null=True, blank=True)
    tracking_number = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(
        max_length=25, 
        blank=True, 
        null=True, 
        choices=[('pending', 'Pending'), ('shipped', 'Shipped')], 
        default="PENDING"
    ) 

    def __str__(self):
        return f"Shipping for Order: {self.order}"

class Payment(models.Model):
    order = models.OneToOneField(Order, related_name="payment", on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(
        max_length=25, 
        blank=True, 
        null=True, 
        choices=[('pending', 'Pending'), ('completed', 'Completed')], 
        default="PENDING"
    ) 
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    amount_paid = models.DecimalField(
        decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
        max_digits=settings.DEFAULT_MAX_DIGITS,
        null=True, 
        blank=True, 
        help_text="", 
    )

    def __str__(self):
        return f"Payment for Order: {self.order}"
