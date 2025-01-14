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
    customer_coupons = models.JSONField(
        blank=True, 
        null=True, 
        help_text="e.g. ['WELCOME25', 'FREESHIP']"
        ) 

    delivery_address = models.TextField(blank=True, help_text="Delivery address")
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


    tax_details = models.JSONField(
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

    currency = models.CharField(max_length=100, help_text="Currency for calculation requirements & validation. e.g. SGD", default=settings.DEFAULT_CURRENCY)
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 


    def __str__(self):
        return f"{self.order_id} - {self.shipping_address} ( {self.status} )"

    def to_domain(self):
        line_items = [
            domain_models.LineItem(
                _id=uuid.uuid4,
                _product_sku=order_line.product_sku,
                _product_name=order_line.product_name,
                _product_category=order_line.product_category,
                _options=json.loads(order_line.options),
                _product_price=value_objects.Money(
                    amount=order_line.product_price,
                    currency=self.currency),
                _order_quantity=order_line.order_quantity,
                _is_free_gift=order_line.is_free_gift,
                _is_taxable=order_line.is_taxable,
                package=value_objects.Package(
                    weight=order_line.weight,
                    dimensions=(order_line.length, order_line.width, order_line.height)
                )
            )
            for order_line in self.line_items.all()
        ]

        order = domain_models.Order(
            _order_id=self.order_id,
            destination=value_objects.Address(
                address=self.delivery_address,
                city=self.delivery_city,
                postal=self.delivery_postal,
                state=self.delivery_state,
                country=self.delivery_country
            ),
            line_items=line_items,
            customer_details=value_objects.CustomerDetails(
                first_name=self.customer_first_name,
                last_name=self.customer_last_name,
                email=self.customer_email
            ),
            shipping_details=value_objects.ShippingDetails(
                method=self.shipping_method,
                delivery_time=self.shipping_delivery_time,
                cost=self.shipping_cost
            ),
            payment_details=value_objects.PaymentDetails(
                method=self.payment_method,
                paid_amount=value_objects.Money(
                    amount=self.payment_amount,
                    currency=self.currency
                    ),
                transaction_id=self.payment_reference
            ),
            _status=self.order_status,
            _cancellation_reason=self.cancellation_reason,
            _total_discounts_fee=value_objects.Money(
                amount=self.total_discounts_fee,
                currency=self.currency
            ),
            _offer_details=self.offer_details,
            _tax_details=self.tax_details,
            _tax_amount=self.tax_amount,
            _total_amount=value_objects.Money(
                amount=self.total_amount,
                currency=self.currency
            ),
            _final_amount=value_objects.Money(
                amount=self.final_amount,
                currency=self.currency
            ),
            _shipping_reference=self.shipping_tracking_reference,
            _currency=self.currency,
            _coupon_codes=self.customer_coupons,
            _date_created=self.date_created,
            _date_modified=self.date_modified
        ) 
        
        
        return order 

    @staticmethod
    def from_domain(order):
        order_model, created = Order.objects.update_or_create(
            id=order.order_id,
            defaults={ 
                "order_status": order.order_status,
                "cancellation_reason": order.cancellation_reason,
                "customer_first_name": order.customer_details.first_name,
                "customer_last_name": order.customer_details.last_name,
                "customer_email": order.customer_details.email,
                "customer_coupons": order.customer_coupons,
                "delivery_address": order.destination.address,
                "delivery_city": order.destination.city,
                "delivery_postal": order.destination.postal,
                "delivery_country": order.destination.country,
                "delivery_state": order.destination.state,
                "total_discounts_fee": order.total_discounts_fee.amount,
                "shipping_method": order.shipping_details.method,
                "shipping_delivery_time": order.shipping_details.delivery_time,
                "shipping_cost": order.shipping_details.cost,
                "tax_details": order.tax_details,
                "tax_amount": order.tax_amount.amount,
                "total_amount": order.total_amount.amount,
                "offer_details": order.offer_details,
                "final_amount": order.final_amount.amount,
                "payment_method": order.payment_details.method,
                "payment_reference": order.payment_details.transaction_id,
                "payment_amount": order.payment_details.paid_amount,
                "currency": order.currency,
                "date_created": order.date_created,
                "date_modified": order.date_modified
            }
        )

        for line_item in order.line_items:
            OrderLine.from_domain(line_item, order.order_id)




class OrderLine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #uuid for global unique id
    order = models.ForeignKey(
        "order_management.Order", 
        on_delete=models.CASCADE,
        related_name="line_items", 
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
    total_price = models.DecimalField(
        decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
        max_digits=settings.DEFAULT_MAX_DIGITS,
        null=True, 
        blank=True, 
        help_text="Total price w/o discounts; to apply discount per Order", 
    )

    def __str__(self):
        return f"Item {self.options} ({self.quantity})"

    @staticmethod
    def from_domain(line_item, order_id):
        orderline_model, created = OrderLine.objects.update_or_create(
            id=line_item.get_id(),
            defaults={
                "product_sku": line_item.product_sku,
                "product_name": line_item.product_name,
                "product_category": line_item.product_category,
                "is_free_gift": line_item.is_free_gift,
                "is_taxable": line_item.is_taxable,
                "options": line_item.options,
                "product_price": line_item.product_price,
                "order_quantity": line_item.order_quantity,
                "package_weight": line_item.package.weight,
                "package_length": line_item.package.dimensions[0],
                "package_width": line_item.package.dimensions[1],
                "package_height": line_item.package.dimensions[2],
                "total_price": line_item.total_price,
                "order_id": order_id
            }

        )


        return orderline_model

