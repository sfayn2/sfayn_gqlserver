from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(
        "order.Order", 
        on_delete=models.CASCADE,
        related_name="order2orderitem", 
        null=True, 
        blank=True
    )
    product_variant = models.ForeignKey(
        'product.VariantItem', 
        on_delete=models.CASCADE, 
        related_name="prodvariant2orderitem"
    )
    quantity = models.IntegerField(null=True)
    locked_in_price = models.FloatField(null=True, blank=True, help_text="Locked-In Price, This wont use the new product price once item is ordered")
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        related_name="user2orderitem"
    )
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"Item {self.product_variant} ({self.quantity})"


class Order(models.Model):

    class Status(models.IntegerChoices):
        WAITING_FOR_PAYMENT = 0
        PAID = 1
        PROCESSING = 2
        SHIPPED_OUT = 3
        REFUNDED = 4
        CANCEL = 5
        COMPLETED = 6

    id = models.AutoField(primary_key=True)
    payment_method = models.ForeignKey(
        "payment.PaymentMethod", 
        on_delete=models.CASCADE,
        related_name="payment2order", 
        null=True, 
        blank=True
    )
    shipping_method = models.ForeignKey(
        "shipping.Method", 
        on_delete=models.CASCADE,
        related_name="shipping2order", 
        null=True, 
        blank=True
    )
    discount = models.ManyToManyField(
        "discount.Discount", 
        related_name="discount2order", 
        blank=True
    )

    shipping_address = models.ForeignKey(
        "accounts.Address", 
        on_delete=models.CASCADE,
        related_name="address2order", 
        null=True, 
        blank=True,
        help_text="delivery address"
    )
    tax = models.ForeignKey(
        "tax.Tax", 
        on_delete=models.CASCADE,
        related_name="tax2order", 
        null=True, 
        blank=True,
        help_text="Country tax applied"
    )
    shipping_fee = models.FloatField(null=True, blank=True, help_text="locked-in shipping fee")
    discount_fee = models.FloatField(null=True, blank=True, help_text="locked-in discount fee")
    tax_rate = models.FloatField(null=True, blank=True, help_text="locked-in tax rate")
    total_amount = models.FloatField(null=True, blank=True)
    notes = models.TextField(help_text="Customer notes to seller", blank=True)
    status = models.IntegerField(
        blank=True, 
        null=True, 
        choices=Status.choices
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="user2order"
    )
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"OrderID:{self.id} - {self.shipping_address} ( {self.get_status_display()} )"


