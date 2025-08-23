from django.db import models
from django.contrib.auth.models import User
import uuid, json
from decimal import Decimal
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

    customer_id = models.CharField(max_length=150, blank=True, null=True)
    customer_first_name = models.CharField(max_length=255, blank=True, null=True)
    customer_last_name = models.CharField(max_length=255, blank=True, null=True)
    customer_email = models.EmailField(max_length=255, blank=True, null=True)
    coupons = models.CharField(
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

    shipping_method = models.CharField(max_length=50, null=True, blank=True, help_text="Customer shipping option (not internal shipping method), i.e. Free Shipping, Local Pickup", choices=enums.ShippingMethod.choices)
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
    payment_status = models.CharField(max_length=50, null=True, blank=True, choices=enums.PaymentStatus.choices)

    currency = models.CharField(max_length=50, help_text="Currency for calculation requirements & validation. e.g. SGD")
    tenant_id = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 


    def __str__(self):
        return f"Order {self.order_id} | {self.customer_first_name} {self.customer_last_name} | Status {self.order_status}  | Total: {self.final_amount} {self.currency}"

class OrderLine(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #uuid for global unique id
    order = models.ForeignKey(
        "order_management.Order", 
        on_delete=models.CASCADE,
        related_name="line_items", 
        null=True, 
        blank=True
    )

    vendor_id = models.CharField(max_length=150)
    vendor_name = models.CharField(max_length=200, help_text="can use to check if product belongs to same vendor")
    vendor_country = models.CharField(max_length=200, help_text="can use to determine if shipping is domestic compared w shipping destination")
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
        unique_together = ("product_sku", "order")

    def __str__(self):
        return f"{self.order.order_id} | {self.product_name} (SKU: {self.product_sku}) | Quantity: {self.order_quantity} | Total: {self.product_price * self.order_quantity} {self.product_currency}"


#==============
# for Vendor Snapshots
#==============
class VendorDetailsSnapshot(models.Model):
    vendor_id = models.CharField(max_length=150)
    tenant_id = models.CharField(max_length=150)
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=50, help_text="Can use to determine if the order is domestic compared w destination")
    is_active = models.BooleanField(default=True, help_text="To quickly control whether the is valid")
    last_update_dt = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.vendor_id} | {self.name} | IsActive: {self.is_active} | {self.last_update_dt}"

class VendorCouponSnapshot(models.Model):
    vendor_id = models.CharField(max_length=150)
    tenant_id = models.CharField(max_length=150)
    offer_id = models.CharField(max_length=150)
    coupon_code = models.CharField(max_length=50, help_text="e.g WELCOME25")
    start_date = models.DateTimeField(help_text="Only valid on start of this date")
    end_date = models.DateTimeField(help_text="Only valid on before end date")
    is_active = models.BooleanField(default=False, help_text="To quickly control whether this offer is still valid")
    last_update_dt = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.tenant_id} | {self.vendor_id} | {self.coupon_code} | Validity: {self.start_date} - {self.end_date} | Active: {self.is_active} | LastUpdate: {self.last_update_dt}"

class VendorOfferSnapshot(models.Model):
    vendor_id = models.CharField(max_length=150)
    tenant_id = models.CharField(max_length=150)
    offer_id = models.CharField(max_length=150)
    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=150, help_text="this is also being used to associate implementation handler and offer Type")
    offer_type = models.CharField(max_length=50, choices=enums.OfferType.choices)
    discount_value = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            help_text="Percentage or Fix amount?", 
            default=Decimal("0.0")
        )
    conditions = models.CharField(max_length=150, help_text='ex. min_purchase, applicable_products')
    stackable = models.BooleanField(default=False, help_text="Set to True, To combine w other stackable")
    priority = models.PositiveIntegerField(default=0, help_text="The highest number will be prioritized on multistack or single stack")
    required_coupon = models.BooleanField(default=False, help_text="Set to True, To make use of coupons to apply")
    start_date = models.DateTimeField(help_text="Only valid on start of this date; To ignore if required_coupon is True", blank=True, null=True)
    end_date = models.DateTimeField(help_text="Only valid on before end date; To ignore if required_coupon is True", blank=True, null=True)
    is_active = models.BooleanField(default=False, help_text="To quickly control whether this offer is still valid")
    last_update_dt = models.DateTimeField(auto_now=True) 


    def __str__(self):
        return f"{self.tenant_id} | {self.vendor_id} | {self.name} ( {self.offer_type} ) | Required Coupon : {self.required_coupon} | {self.start_date} - {self.end_date} | Is Active: {self.is_active} | LastUpdate: {self.last_update_dt}"

class VendorPaymentOptionSnapshot(models.Model):
    vendor_id = models.CharField(max_length=150)
    tenant_id = models.CharField(max_length=150)

    option_name = models.CharField(max_length=255, help_text="Just a name of this payment Option. e.g. Credit Card (Stripe) ")
    method = models.CharField(max_length=50, null=True, blank=True, choices=enums.PaymentMethod.choices)
    provider = models.CharField(max_length=150, help_text="this is also being used to associate implementation handler and payment method")
    conditions = models.CharField(max_length=150, help_text='ex. { "country": "US" }')
    is_active = models.BooleanField(default=False, help_text="To quickly control whether this option is still valid")
    last_update_dt = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.tenant_id} | {self.vendor_id} | {self.option_name}  | LastUpdate: {self.last_update_dt}"


class VendorTaxOptionSnapshot(models.Model):
    vendor_id = models.CharField(max_length=150)
    tenant_id = models.CharField(max_length=150)

    tax_type = models.CharField(max_length=50, null=True, blank=True, choices=enums.TaxType.choices)
    provider = models.CharField(max_length=150, help_text="this is also being used to associate implementation handler and tax type")
    inclusive = models.BooleanField(default=False)

    rate = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            help_text="", 
            default=Decimal("0.0")
        )
    conditions = models.CharField(max_length=150, help_text='ex. { "state_tax_rate": { "CA": 0.075, "NY": 0.04, "TX": 0.0625 } }')

    is_active = models.BooleanField(default=False, help_text="To quickly control whether this option is still valid")
    last_update_dt = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.tenant_id} | {self.vendor_id} | {self.tax_type} | {self.conditions} | LastUpdate: {self.last_update_dt}"

class VendorShippingOptionSnapshot(models.Model):
    vendor_id = models.CharField(max_length=150)
    tenant_id = models.CharField(max_length=150)

    option_name = models.CharField(max_length=255, help_text="Just a name of this shipping Option. e.g. MyStandard")
    method = models.CharField(max_length=50, null=True, blank=True, choices=enums.ShippingMethod.choices)
    provider = models.CharField(max_length=150, help_text="this is also being used to associate implementation handler and shipping method")

    base_cost = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            help_text="", 
            default=Decimal("0.0")
        )
    currency = models.CharField(max_length=50, help_text="Default currency specific to this Shipping option base cost or flat rate", default=settings.DEFAULT_CURRENCY)

    conditions = models.CharField(max_length=150, help_text='ex. { "max_weight": 30 }')

    flat_rate = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            help_text="", 
            default=Decimal("0.0")
        )
    delivery_time = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False, help_text="To quickly control whether this option is still valid")
    last_update_dt = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.tenant_id} | {self.vendor_id} | {self.option_name} | {self.delivery_time} | {self.conditions} | LastUpdate: {self.last_update_dt}"

class VendorProductSnapshot(models.Model):
    product_id = models.CharField(max_length=150)
    vendor_id = models.CharField(max_length=150)
    tenant_id = models.CharField(max_length=150)
    product_sku = models.CharField(max_length=50)
    product_name = models.CharField(max_length=255)
    product_category = models.CharField(max_length=100, help_text="some countries uses category to calculate tax")
    options = models.CharField(max_length=150, help_text='ex. {"Size": "M", "Color": "RED"}') # anticipated to have complex tables to support multi dimension variants, decided to use JSONField
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    product_currency = models.CharField(max_length=50, help_text="Currency for calculation requirements & validation. e.g. SGD")
    package_weight = models.CharField(max_length=100, null=True, blank=True, help_text="value should be coming from product itself or to fill in later once it goes to warehouse fulfillment?")
    package_length = models.CharField(max_length=100, null=True, blank=True, help_text="value should be coming from product itself or to fill in later once it goes to warehouse fulfillment? ")
    package_width = models.CharField(max_length=100, null=True, blank=True, help_text="value should be coming from product itself or to fill in later once it goes to warehouse fulfillment?")
    package_height = models.CharField(max_length=100, null=True, blank=True, help_text="value should be coming from product itself or to fill in later once it goes to warehouse fulfillment?")
    is_active = models.BooleanField(default=True)
    last_update_dt = models.DateTimeField(auto_now=True) 

    class Meta:
        unique_together = ('product_sku', 'tenant_id', 'vendor_id') #ensure one default per addres type

    def __str__(self):
        return f"({self.tenant_id} | {self.vendor_id}) | {self.product_sku} | {self.product_name} | {self.stock} | {self.is_active}"


#===========================
# For Customer snapshot
#===================
class CustomerDetailsSnapshot(models.Model):
    customer_id = models.CharField(max_length=150)
    tenant_id = models.CharField(max_length=150)
    user_id = models.CharField(max_length=150, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    last_update_dt = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.tenant_id} | {self.customer_id} | {self.first_name} {self.last_name} | {self.email}"

class CustomerAddressSnapshot(models.Model):
    ADDRESS_TYPE_CHOICES = (
        ('billing', 'Billing'),
        ('shipping', 'Shipping'),
    )

    customer_id = models.CharField(max_length=150)

    address_type = models.CharField(
        max_length=10,
        choices=ADDRESS_TYPE_CHOICES
    )

    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=10, blank=True, null=True)
    postal = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_update_dt = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.customer_id} | {self.address_type.capitalize()} Address: {self.street}, {self.city}, {self.country}"

    class Meta:
        unique_together = ('customer_id', 'address_type', 'is_default') #ensure one default per addres type

# =========
# Local Authorization / Scope Based
# =========
class UserAuthorizationSnapshot(models.Model):
    user_id = models.CharField(max_length=150)
    permission_codename = models.CharField(max_length=255)
    tenant_id = models.CharField(max_length=150)
    scope = models.CharField(max_length=150, help_text='ex. { "customer_id": "c-1234" }')
    is_active = models.BooleanField(default=True)
    last_update_dt = models.DateTimeField(auto_now=True) 

    class Meta:
        unique_together = ('user_id', 'permission_codename', 'scope') 

    def __str__(self):
        return f"{self.tenant_id} | {self.user_id} | {self.permission_codename} | {self.scope}"