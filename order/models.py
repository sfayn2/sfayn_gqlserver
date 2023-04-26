from django.db import models
from django.contrib.auth.models import User
from utils.utils import path_and_rename

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
    product_price = models.FloatField(null=True, blank=True, help_text="sale price, exclusive of tax")
    product_options = models.CharField(max_length=50, null=True, blank=True) # Red/Blue?
    product_img_upload = models.ImageField(upload_to=path_and_rename, null=True, blank=True, help_text="Primary img")
    product_img_url = models.CharField(max_length=300, null=True, blank=True, help_text="secondary img") 
    #Locked product info


    discount = models.ManyToManyField(
        "discount.Discount", 
        related_name="discount2orderitem", 
        blank=True,
        help_text="any discount per item"
    )
    #Locked multiple discount info??
    discount_name = models.CharField(max_length=150, help_text="Multiple discounts used. ex. DiscountTypeBuyXGetX,DiscountTypeFixedAmount")
    discount_total = models.FloatField(null=True, blank=True, help_text="total discounts fee")
    #Locked discount info

    total_amount = models.FloatField(null=True, blank=True, help_text="(original_price*quantity)-discount_fee ") 
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

    discount = models.ManyToManyField(
        "discount.Discount", 
        related_name="discount2order", 
        blank=True,
        help_text="discounts per order"
    )
    discount_names = models.CharField(max_length=150, help_text="Multiple discounts used. ex. DiscountTypeVoucher")

    shipping_method_id = models.IntegerField(null=True, blank=True)
    shipping_title = models.CharField(max_length=50, help_text="ex. Free shipping, Local pickup")
    shipping_desc = models.CharField(max_length=150)
    shipping_cost = models.FloatField(null=True, blank=True, help_text="cost or overall cost?")

    shipping_address = models.ForeignKey(
        "accounts.Address", 
        on_delete=models.CASCADE,
        related_name="address2order", 
        null=True, 
        blank=True,
        help_text="delivery address"
    )
    #Locked shipping address info
    shipping_address = models.TextField()
    shipping_postal = models.CharField(max_length=50)
    shipping_country = models.CharField(max_length=50)
    shipping_region = models.CharField(max_length=50)
    #Locked shipping address info

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
    tax_rate = models.FloatField(null=True, blank=True, help_text="N% tax rate per order?", verbose_name="Rate(%)")
    #Locked tax info

    order_items_total = models.FloatField(null=True, blank=True, help_text="total items without order discounts and tax")
    order_shipping_total = models.FloatField(null=True, blank=True, help_text="shipping fee")
    order_discounts_total = models.FloatField(null=True, blank=True, help_text="total discounts fee")
    order_amount_total = models.FloatField(null=True, blank=True, help_text="order overall total amount") 
    order_paid_total = models.FloatField(null=True, blank=True, help_text="amount paid by customer") 
    order_customer_note = models.TextField(help_text="Customer notes to seller", blank=True)
    order_status = models.IntegerField(
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


