from django.db import models
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
    return_reason = models.CharField(max_length=255, blank=True, null=True)

    #refund need?
    refund_reason = models.CharField(max_length=255, blank=True, null=True)

    customer_first_name = models.CharField(max_length=255)
    customer_last_name = models.CharField(max_length=255)
    customer_email = models.EmailField(max_length=255, blank=True, null=True)
    customer_coupons = models.CharField(max_length=100, help_text="Customer entered coupons, just provide a list i.e WELCOME01,FREESHIP01")

    delivery_address = models.TextField(blank=True, help_text="Delivery address")
    delivery_city = models.CharField(max_length=50, blank=True, null=True, help_text="Optional for other countries (e.g. Singapore)")
    delivery_postal = models.CharField(max_length=50, blank=True, null=True, help_text="some countries dont use this (e.g Ireland?)")
    delivery_country = models.CharField(max_length=50)
    delivery_state = models.CharField(max_length=10, blank=True, null=True, help_text="Mandatory in countries like US, Canada, India but irrelevant in small countries")

    subtotal = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            null=True, 
            blank=True, 
            help_text="total items w/o order discounts and tax", 
    )
    total_discounts_fee = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            null=True, 
            blank=True, 
            help_text="total discounts fee per order", 
    )

    shipping_method = models.CharField(max_length=50, null=True, blank=True, help_text="i.e. Free Shipping, Local Pickup", choices=enums.ShippingMethod.choices)
    shipping_delivery_time = models.CharField(max_length=150, null=True, blank=True, help_text="i.e. 2-3 days delivery")
    shipping_cost = models.DecimalField(
        decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
        max_digits=settings.DEFAULT_MAX_DIGITS,
        null=True, 
        blank=True, 
        help_text="", 
    )


    tax_desc = models.CharField(max_length=20, help_text="GST 9%, VAT, ?")
    tax_amount = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            null=True, 
            blank=True, 
            help_text="tax amount", 
        )

    total_amount = models.DecimalField(
        decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
        max_digits=settings.DEFAULT_MAX_DIGITS,
        null=True, 
        blank=True, 
        help_text="overall total", 
    )

    offer_details = models.JSONField(
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

    total_paid = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            null=True, 
            blank=True, 
            help_text="amount paid by customer", 
    )

    currency = models.CharField(max_length=100, help_text="Currency for calculation requirements & validation. e.g. SGD", default=settings.DEFAULT_CURRENCY)
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    class Meta:
        permissions = [
            ("default_shipping_option_policy", "Can use default shipping option policy"),
            ("default_offer_policy", "Can use default offer/coupon policy"),
        ]

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
    product_name = models.CharField(max_length=255)
    product_category = models.CharField(max_length=100, help_text="some countries uses category to calculate tax")
    is_free_gift = models.BooleanField(default=False)
    is_taxable = models.BooleanField(default=True)
    options = models.JSONField(help_text='ex. {"Size": "M", "Color": "RED"}') # anticipated to have complex tables to support multi dimension variants, decided to use JSONField
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_quantity = models.PositiveIntegerField(null=True)
    package_weight = models.CharField(max_length=100, null=True, blank=True, help_text="value should be coming from product itself or to fill in later once it goes to warehouse fulfillment?")
    package_length = models.CharField(max_length=100, null=True, blank=True, help_text="value should be coming from product itself or to fill in later once it goes to warehouse fulfillment? ")
    package_width = models.CharField(max_length=100, null=True, blank=True, help_text="value should be coming from product itself or to fill in later once it goes to warehouse fulfillment?")
    package_height = models.CharField(max_length=100, null=True, blank=True, help_text="value should be coming from product itself or to fill in later once it goes to warehouse fulfillment?")
    discounts_fee = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            null=True, 
            blank=True, 
            help_text="discounts per line item; right now only used for record keeping.", 
        )
    total_price = models.DecimalField(
        decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
        max_digits=settings.DEFAULT_MAX_DIGITS,
        null=True, 
        blank=True, 
        help_text="Total price w/o discounts; to apply discount per Order", 
    )

    def __str__(self):
        return f"Item {self.product_variant} ({self.quantity})"

class Payment(models.Model):
    PAYMENT_STATUS = (
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("REFUNDED", "Refunded"),
        ("FAILED", "Failed")
    )
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(
        "order.Order", 
        on_delete=models.CASCADE,
        related_name="payments", 
        null=True, 
        blank=True
    )
    payment_method = models.CharField(max_length=50, null=True, blank=True, choices=enums.PaymentMethod.choices)
    amount = models.DecimalField(
        decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
        max_digits=settings.DEFAULT_MAX_DIGITS,
        null=True, 
        blank=True, 
        help_text="amount paid in this transaction", 
    )
    transaction_id = models.CharField(
        max_length=25, 
        blank=True, 
        null=True, 
    ) 
    status = models.CharField(
        max_length=25, 
        blank=True, 
        null=True, 
        choices=PAYMENT_STATUS
    ) 
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 