from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(
        "order.Order", 
        on_delete=models.CASCADE,
        related_name="_order2orderitem", 
        null=True, 
        blank=True
    )
    product_variant = models.OneToOneField(
        'product.ProductVariantItem', 
        on_delete=models.CASCADE, 
        related_name="_prodvariant2cart"
    )
    quantity = models.IntegerField(null=True)
    locked_in_price = models.FloatField(null=True, blank=True, help_text="Locked-In Price, This wont use the new product price once item is ordered")
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        related_name="_user2orderitem"
    )
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return "Order({}) ShopCart({})".format(self.order, self.shopcart)


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
        related_name="_payment2order", 
        null=True, 
        blank=True
    )
    customer_address = models.ForeignKey(
        "customer.CustomerAddress", 
        on_delete=models.CASCADE,
        related_name="_customer2order", 
        null=True, 
        blank=True
    )
    total_amount = models.FloatField(null=True, blank=True)
    status = models.IntegerField(
        blank=True, 
        null=True, 
        choices=Status.choices
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="_user2order"
    )
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return "PaymentMethod({}) CustomerAddress({}) TotalAmount({}) Status({})".format(
            self.payment_method,
            self.customer_address,
            self.total_amount,
            self.status
        )


