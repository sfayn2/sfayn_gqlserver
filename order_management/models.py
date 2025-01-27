from django.db import models
import uuid
import json
from django.conf import settings
from ddd.order_management.domain import enums, models as domain_models, value_objects

# Create your models here.

class Order(models.Model):
    order_id = models.CharField(max_length=100, primary_key=True, help_text="ORD-1234")

    order_status = models.CharField(
        max_length=25, 
        blank=True, 
        null=True, 
        choices=enums.OrderStatus.choices, 
        default=enums.OrderStatus.DRAFT
    ) 
    cancellation_reason = models.CharField(max_length=255, blank=True, null=True, help_text="both entity like vendor or customer can cancel the order?")

    customer_first_name = models.CharField(max_length=255)
    customer_last_name = models.CharField(max_length=255)
    customer_email = models.EmailField(max_length=255, blank=True, null=True)
    customer_coupons = models.CharField(
        max_length=150,
        blank=True, 
        null=True, 
        help_text=r'e.g. ["WELCOME25", "FREESHIP"]'
        ) 

    delivery_street = models.TextField(blank=True, help_text="Delivery address")
    delivery_city = models.CharField(max_length=50, blank=True, null=True, help_text="Optional for other countries (e.g. Singapore)")
    delivery_postal = models.CharField(max_length=50, blank=True, null=True, help_text="some countries dont use this (e.g Ireland?)")
    delivery_country = models.CharField(max_length=50)
    delivery_state = models.CharField(max_length=10, blank=True, null=True, help_text="Mandatory in countries like US, Canada, India but irrelevant in small countries")

    shipping_method = models.CharField(max_length=50, null=True, blank=True, help_text="i.e. Free Shipping, Local Pickup", choices=enums.ShippingMethod.choices)
    shipping_delivery_time = models.CharField(max_length=150, null=True, blank=True, help_text="i.e. 2-3 days delivery")
    shipping_cost = models.DecimalField(
        decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
        max_digits=settings.DEFAULT_MAX_DIGITS,
        null=True, 
        blank=True, 
        help_text="", 
    )
    shipping_tracking_reference = models.CharField(max_length=50, null=True, blank=True, help_text="")


    tax_details = models.CharField(
        max_length=150,
        blank=True, 
        null=True, 
        help_text='e.g. ["GST (9%)", "Local State (2%)"]'
        ) 
    tax_amount = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            null=True, 
            blank=True, 
            help_text="tax amount", 
        )

    total_discounts_fee = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            null=True, 
            blank=True, 
            help_text="total discounts fee per order", 
    )


    total_amount = models.DecimalField(
        decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
        max_digits=settings.DEFAULT_MAX_DIGITS,
        null=True, 
        blank=True, 
        help_text="overall total", 
    )

    offer_details = models.CharField(
        max_length=150,
        blank=True, 
        null=True, 
        help_text='e.g. ["Free Shipping applied", "Discount applied: $20.00"]'
        ) 

    final_amount = models.DecimalField(
        decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
        max_digits=settings.DEFAULT_MAX_DIGITS,
        null=True, 
        blank=True, 
        help_text="overall total - discounts + ship cost + tax, etc. ?", 
    )

    payment_method = models.CharField(max_length=50, null=True, blank=True, choices=enums.PaymentMethod.choices)
    payment_reference = models.CharField(
        max_length=25, 
        blank=True, 
        null=True, 
        help_text="payment transaction id"
    ) 
    payment_amount = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            null=True, 
            blank=True, 
            help_text="amount paid by customer", 
    )

    currency = models.CharField(max_length=50, help_text="Currency for calculation requirements & validation. e.g. SGD")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 


    def __str__(self):
        return f"{self.order_id} - {self.delivery_street} ( {self.order_status} )"

class OrderLine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #uuid for global unique id
    order = models.ForeignKey(
        "order_management.Order", 
        on_delete=models.CASCADE,
        related_name="line_items", 
        null=True, 
        blank=True
    )

    vendor_name = models.CharField(max_length=200, help_text="can use to check if product belongs to same vendor")
    product_sku = models.CharField(max_length=50)
    product_name = models.CharField(max_length=255)
    product_category = models.CharField(max_length=100, help_text="some countries uses category to calculate tax")
    is_free_gift = models.BooleanField(default=False)
    is_taxable = models.BooleanField(default=True)
    options = models.CharField(max_length=150, help_text='ex. {"Size": "M", "Color": "RED"}') # anticipated to have complex tables to support multi dimension variants, decided to use JSONField
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_currency = models.CharField(max_length=50, help_text="Currency for calculation requirements & validation. e.g. SGD")
    order_quantity = models.PositiveIntegerField(null=True)
    package_weight = models.CharField(max_length=100, null=True, blank=True, help_text="value should be coming from product itself or to fill in later once it goes to warehouse fulfillment?")
    package_length = models.CharField(max_length=100, null=True, blank=True, help_text="value should be coming from product itself or to fill in later once it goes to warehouse fulfillment? ")
    package_width = models.CharField(max_length=100, null=True, blank=True, help_text="value should be coming from product itself or to fill in later once it goes to warehouse fulfillment?")
    package_height = models.CharField(max_length=100, null=True, blank=True, help_text="value should be coming from product itself or to fill in later once it goes to warehouse fulfillment?")
    total_price = models.DecimalField(
        decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
        max_digits=settings.DEFAULT_MAX_DIGITS,
        null=True, 
        blank=True, 
        help_text="Total price w/o discounts; to apply discount per Order", 
    )

    class Meta:
        unique_together = ("product_sku", "order_id")

    def __str__(self):
        return f"{self.order.order_id} - {self.product_sku} {self.options} ({self.order_quantity})"


