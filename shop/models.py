from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ShopCart(models.Model):
    id = models.AutoField(primary_key=True)
    product_variant = models.ForeignKey('product.ProductVariant', on_delete=models.CASCADE, related_name="prodvariant2cart")
    quantity = models.IntegerField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2cart")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 


class ShopOrderItems(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey("shop.ShopOrder", related_name="order2orderitems", null=True, blank=True)
    shopcart = models.ForeignKey("shop.ShopCart", related_name="cart2orderitems", null=True, blank=True) 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2cart")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 


class ShopOrder(models.Model):
    STATUS_CHOICES = (
        (0, "Waiting for Payment"),
        (1, "Paid"),
        (2, "Processing"),
        (3, "Shipped Out"),
        (4, "Refunded"),
        (5, "Cancel"),
        (6, "Completed"),
    )
    id = models.AutoField(primary_key=True)
    payment_method = models.ForeignKey("payment.PaymentMethod", related_name="payment2order", null=True, blank=True)
    customer_address = models.ForeignKey("customer.CustomerAddress", related_name="customer2order"null=True, blank=True)
    total_amount = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length="50", blank=True, null=True, choices=STATUS_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2order")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 


