from django.db import models
from django.contrib.auth.models import User
from utils import path_and_rename

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
    order_quantity = models.IntegerField(null=True)

    product_variant = models.ForeignKey(
        'product.VariantItem', 
        on_delete=models.CASCADE, 
        related_name="prodvariant2orderitem"
    )
    #Locked product info
    product_sn = models.CharField(max_length=25, null=True, blank=True)
    product_price = models.FloatField(null=True, blank=True, help_text="undiscounted price")
    product_options = models.CharField(max_length=50, null=True, blank=True) # Red/Blue?
    product_variant_name = models.CharField(max_length=50, null=True, blank=True) # COLOR?
    product_img_upload = models.ImageField(upload_to=path_and_rename, null=True, blank=True, help_text="Primary img")
    product_img_url = models.CharField(max_length=300, null=True, blank=True, help_text="secondary img") 
    #product_weight ?
    #product_length

    #Locked product info


    discounts = models.FloatField(null=True, blank=True, help_text="discounts per item") 
    discounted_price = models.FloatField(null=True, blank=True, help_text="(product_price*order_quantity)-discounts_fee ") 
    total = models.FloatField(null=True, blank=True, help_text="it can be the discounted price or product original price?") 

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
    #Locked payment info
    payment_method_name = models.CharField(max_length=50, null=True, blank=True)



    tax = models.ForeignKey(
        "tax.Tax", 
        on_delete=models.CASCADE,
        related_name="tax2order", 
        null=True, 
        blank=True,
        help_text="Country tax applied"
    )
    #Locked tax info
    tax_name = models.CharField(max_length=20, help_text="GST, VAT, ?")
    tax_country = models.CharField(max_length=50)
    #Locked tax info

    subtotal = models.FloatField(null=True, blank=True, help_text="total items without order discounts and tax")
    discounts = models.FloatField(null=True, blank=True, help_text="total discounts fee per order")
    discounted_subtotal = models.FloatField(null=True, blank=True, help_text="discounted subtotal")
    tax_rate = models.FloatField(null=True, blank=True, help_text="N% tax rate per order?", verbose_name="Rate(%)")
    total_tax = models.FloatField(null=True, blank=True, help_text="tax amount")
    shipping = models.FloatField(null=True, blank=True, help_text="shipping fee")
    total = models.FloatField(null=True, blank=True, help_text="overall total") 
    currency = models.TextField(help_text="USD", blank=True)
    customer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="customer2order"
    )
    amount_paid = models.FloatField(null=True, blank=True, help_text="amount paid by customer") 
    customer_note = models.TextField(help_text="Customer notes to seller", blank=True)
    status = models.IntegerField(
        blank=True, 
        null=True, 
        choices=Status.choices
    )

    #should always be system user
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="user2order"
    )
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"OrderID:{self.id} - {self.shipping_address} ( {self.get_status_display()} )"


# one order can possibly have multiple fulfillment
class OrderFulfillment(models.Model):

    class Status(models.IntegerChoices):
        NOT_FULFILLED = 0
        FULFILLED = 1
        CANCEL = 2

    order = models.ForeignKey(
        "order.Order", 
        on_delete=models.CASCADE,
        related_name="order2orderfulfill", 
        null=True, 
        blank=True
    )
    tracking_number = models.CharField(max_length=120, blank=True, null=True, help_text="a string fulfillment tracking number")

    fulfillment = models.ForeignKey(
        "fulfillment.Fulfillment", 
        on_delete=models.CASCADE,
        related_name="fulfill2orderfulfill", 
        null=True, 
        blank=True
    )

    #Locked fulfillment info
    name = models.CharField(max_length=20) #can be outsource?
    company_url = models.CharField(max_length=200, blank=True, null=True)
    tracker_url = models.CharField(max_length=200, blank=True, null=True)
    logo = models.ImageField(upload_to=path_and_rename, null=True, blank=True, help_text="company logo")
    #Locked fulfillment info

    #Locked shipping method info
    shipping_method_id = models.IntegerField(null=True, blank=True)
    shipping_title = models.CharField(null=True, blank=True, max_length=50, help_text="ex. Free shipping, Local pickup")
    shipping_desc = models.CharField(null=True, blank=True, max_length=150)
    shipping_cost = models.FloatField(null=True, blank=True, help_text="cost or overall cost?")
    #Locked shipping method info

    shipping_address = models.ForeignKey(
        "accounts.Address", 
        on_delete=models.CASCADE,
        related_name="address2orderfulfillment", 
        null=True, 
        blank=True,
        help_text="delivery address"
    )
    #Locked shipping address info
    shipping_address = models.TextField(blank=True)
    shipping_postal = models.CharField(max_length=50)
    shipping_country = models.CharField(max_length=50)
    shipping_region = models.CharField(max_length=50)
    #Locked shipping address info

    status = models.IntegerField(
        blank=True, 
        null=True, 
        choices=Status.choices
    )

    #should always be system user??
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="user2orderfulfillment"
    )
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 
