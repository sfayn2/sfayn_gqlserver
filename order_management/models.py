from django.db import models
from django.contrib.auth.models import User
import uuid, json
from decimal import Decimal
from django.conf import settings
from ddd.order_management.domain import enums, models as domain_models, value_objects

# Create your models here.

class Order(models.Model):
    order_id = models.CharField(max_length=100, primary_key=True, help_text="ORD-1234")
    tenant_id = models.CharField(max_length=150)
    checkout_session = models.CharField(max_length=100, null=True, blank=True, help_text="{app}-{identifier} . eg. checkoutapp-1234")

    order_status = models.CharField(
        max_length=25, 
        blank=True, 
        null=True, 
        choices=enums.OrderStatus.choices, 
        default=enums.OrderStatus.DRAFT
    ) 

    # sub status / workflow status
    activity_status = models.CharField(
        max_length=25, 
        blank=True, 
        null=True
    ) 

    customer_id = models.CharField(max_length=150, blank=True, null=True)
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_email = models.EmailField(max_length=255, blank=True, null=True)

    payment_status = models.CharField(max_length=50, null=True, blank=True, choices=enums.PaymentStatus.choices)

    currency = models.CharField(max_length=50, help_text="Currency for calculation requirements & validation. e.g. SGD")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"Order {self.order_id} | {self.customer_name} | Status {self.order_status}"

class LineItem(models.Model):
    order = models.ForeignKey(
        "order_management.Order", 
        on_delete=models.CASCADE,
        related_name="line_items", 
        null=True, 
        blank=True
    )

    product_sku = models.CharField(max_length=50)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_quantity = models.PositiveIntegerField(null=True)

    vendor_name = models.CharField(max_length=200, help_text="can use to check if product belongs to same vendor")

    pickup_address_line1 = models.TextField(blank=True, null=True, help_text="Warehouse/Vendor address")
    pickup_address_line2 = models.TextField(blank=True, null=True, help_text="Warehouse/Vendor address2")
    pickup_address_city = models.CharField(max_length=50, blank=True, null=True, help_text="Optional for other countries (e.g. Singapore)")
    pickup_address_postal = models.CharField(max_length=50, blank=True, null=True, help_text="some countries dont use this (e.g Ireland?)")
    pickup_address_country = models.CharField(max_length=50)
    pickup_address_state = models.CharField(max_length=10, blank=True, null=True, help_text="Mandatory in countries like US, Canada, India but irrelevant in small countries")

    class Meta:
        unique_together = ("product_sku", "order")

    def __str__(self):
        return f"{self.order.order_id} | {self.product_name} (SKU: {self.product_sku}) | Quantity: {self.order_quantity} | Total: {self.product_price * self.order_quantity}"


class Shipment(models.Model):

    shipment_id = models.CharField(max_length=100, primary_key=True, help_text="SH-xxx")

    order = models.ForeignKey(
        "order_management.Order", 
        on_delete=models.CASCADE,
        related_name="shipments", 
        null=True, 
        blank=True
    )

    shipment_address_line1 = models.TextField(blank=True, null=True, help_text="Warehouse/Vendor address")
    shipment_address_line2 = models.TextField(blank=True, null=True, help_text="Warehouse/Vendor address2")
    shipment_address_city = models.CharField(max_length=50, blank=True, null=True, help_text="Optional for other countries (e.g. Singapore)")
    shipment_address_postal = models.CharField(max_length=50, blank=True, null=True, help_text="some countries dont use this (e.g Ireland?)")
    shipment_address_country = models.CharField(max_length=50, blank=True, null=True)
    shipment_address_state = models.CharField(max_length=10, blank=True, null=True, help_text="Mandatory in countries like US, Canada, India but irrelevant in small countries")

    shipment_provider = models.CharField(max_length=25, blank=True, null=True)
    shipment_service_code = models.CharField(max_length=25, blank=True, null=True)
    tracking_reference = models.CharField(max_length=100, blank=True, null=True)

    shipment_amount = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            null=True, 
            blank=True, 
            help_text="shipping amount", 
        )
    shipment_tax_amount = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            null=True, 
            blank=True, 
            help_text="shipping tax amount", 
        )
    shipment_currency = models.CharField(max_length=25, blank=True, null=True)

    shipment_status = models.CharField(
        max_length=25, 
        blank=True, 
        null=True, 
        choices=enums.ShipmentStatus.choices, 
        default=enums.ShipmentStatus.PENDING
    ) 


class ShipmentItem(models.Model):

    shipment_item_id = models.CharField(max_length=100, primary_key=True, help_text="SHI-xxx")

    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="shipment_items")

    line_item = models.ForeignKey(
        "order_management.LineItem", 
        on_delete=models.CASCADE,
        related_name="shipment_allocations", 
        null=True, 
        blank=True
    )

    quantity = models.PositiveIntegerField(null=True)
    allocated_shipping_tax = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            null=True, 
            blank=True, 
            help_text="allocated shipping tax amount", 
        )
    allocated_shipping_tax_currency = models.CharField(max_length=25, blank=True, null=True)


class UserActionLog(models.Model):
    order_id = models.CharField(
        max_length=25, 
    ) 
    action = models.CharField(max_length=50, help_text="should match w permission ?")
    performed_by = models.CharField(max_length=50, help_text="system or user or reviewer or other")
    user_input = models.CharField(max_length=500, help_text='{"comment": "Looks good"}')
    executed_at = models.DateTimeField(auto_now=True) 




# =========
# Local Authorization / Scope Based
# =========
class UserAuthorizationSnapshot(models.Model):
    tenant_id = models.CharField(max_length=150)
    permission_codename = models.CharField(max_length=255)
    scope = models.CharField(max_length=150, help_text='ex. { "role": "vendor" }')
    is_active = models.BooleanField(default=True)
    last_update_dt = models.DateTimeField(auto_now=True) 

    class Meta:
        unique_together = ('tenant_id', 'permission_codename', 'scope') 

    def __str__(self):
        return f"{self.tenant_id} | {self.permission_codename} | {self.scope}"
