# Generated by Django 5.1.4 on 2025-07-11 08:08

import ddd.order_management.domain.enums
import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerDetailsSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.CharField(max_length=150)),
                ('tenant_id', models.CharField(max_length=150)),
                ('user_id', models.CharField(blank=True, max_length=150, null=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('last_update_dt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.CharField(help_text='ORD-1234', max_length=100, primary_key=True, serialize=False)),
                ('order_status', models.CharField(blank=True, choices=ddd.order_management.domain.enums.OrderStatus.choices, default=ddd.order_management.domain.enums.OrderStatus['DRAFT'], max_length=25, null=True)),
                ('cancellation_reason', models.CharField(blank=True, help_text='both entity like vendor or customer can cancel the order?', max_length=255, null=True)),
                ('customer_id', models.CharField(blank=True, max_length=150, null=True)),
                ('customer_first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('customer_last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('customer_email', models.EmailField(blank=True, max_length=255, null=True)),
                ('coupons', models.CharField(blank=True, help_text='e.g. ["WELCOME25", "FREESHIP"]', max_length=150, null=True)),
                ('delivery_street', models.TextField(blank=True, help_text='Delivery address')),
                ('delivery_city', models.CharField(blank=True, help_text='Optional for other countries (e.g. Singapore)', max_length=50, null=True)),
                ('delivery_postal', models.CharField(blank=True, help_text='some countries dont use this (e.g Ireland?)', max_length=50, null=True)),
                ('delivery_country', models.CharField(max_length=50)),
                ('delivery_state', models.CharField(blank=True, help_text='Mandatory in countries like US, Canada, India but irrelevant in small countries', max_length=10, null=True)),
                ('shipping_method', models.CharField(blank=True, choices=ddd.order_management.domain.enums.ShippingMethod.choices, help_text='Customer shipping option (not internal shipping method), i.e. Free Shipping, Local Pickup', max_length=50, null=True)),
                ('shipping_delivery_time', models.CharField(blank=True, help_text='i.e. 2-3 days delivery', max_length=150, null=True)),
                ('shipping_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('shipping_tracking_reference', models.CharField(blank=True, max_length=50, null=True)),
                ('tax_details', models.CharField(blank=True, help_text='e.g. ["GST (9%)", "Local State (2%)"]', max_length=150, null=True)),
                ('tax_amount', models.DecimalField(blank=True, decimal_places=2, help_text='tax amount', max_digits=15, null=True)),
                ('total_discounts_fee', models.DecimalField(blank=True, decimal_places=2, help_text='total discounts fee per order', max_digits=15, null=True)),
                ('total_amount', models.DecimalField(blank=True, decimal_places=2, help_text='overall total', max_digits=15, null=True)),
                ('offer_details', models.CharField(blank=True, help_text='e.g. ["Free Shipping applied", "Discount applied: $20.00"]', max_length=150, null=True)),
                ('final_amount', models.DecimalField(blank=True, decimal_places=2, help_text='overall total - discounts + ship cost + tax, etc. ?', max_digits=15, null=True)),
                ('payment_method', models.CharField(blank=True, choices=ddd.order_management.domain.enums.PaymentMethod.choices, max_length=50, null=True)),
                ('payment_reference', models.CharField(blank=True, help_text='payment transaction id', max_length=25, null=True)),
                ('payment_amount', models.DecimalField(blank=True, decimal_places=2, help_text='amount paid by customer', max_digits=15, null=True)),
                ('payment_status', models.CharField(blank=True, choices=ddd.order_management.domain.enums.PaymentStatus.choices, max_length=50, null=True)),
                ('currency', models.CharField(help_text='Currency for calculation requirements & validation. e.g. SGD', max_length=50)),
                ('tenant_id', models.CharField(max_length=150)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='VendorCouponSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_id', models.CharField(max_length=150)),
                ('tenant_id', models.CharField(max_length=150)),
                ('offer_id', models.CharField(max_length=150)),
                ('coupon_code', models.CharField(help_text='e.g WELCOME25', max_length=50)),
                ('start_date', models.DateTimeField(help_text='Only valid on start of this date')),
                ('end_date', models.DateTimeField(help_text='Only valid on before end date')),
                ('is_active', models.BooleanField(default=False, help_text='To quickly control whether this offer is still valid')),
                ('last_update_dt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='VendorDetailsSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_id', models.CharField(max_length=150)),
                ('tenant_id', models.CharField(max_length=150)),
                ('name', models.CharField(max_length=200)),
                ('country', models.CharField(help_text='Can use to determine if the order is domestic compared w destination', max_length=50)),
                ('is_active', models.BooleanField(default=True, help_text='To quickly control whether the is valid')),
                ('last_update_dt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='VendorOfferSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_id', models.CharField(max_length=150)),
                ('tenant_id', models.CharField(max_length=150)),
                ('offer_id', models.CharField(max_length=150)),
                ('name', models.CharField(max_length=255)),
                ('offer_type', models.CharField(choices=ddd.order_management.domain.enums.OfferType.choices, max_length=50)),
                ('discount_value', models.DecimalField(decimal_places=2, default=Decimal('0.0'), help_text='Percentage or Fix amount?', max_digits=15)),
                ('conditions', models.CharField(help_text='ex. min_purchase, applicable_products', max_length=150)),
                ('stackable', models.BooleanField(default=False, help_text='Set to True, To combine w other stackable')),
                ('priority', models.PositiveIntegerField(default=0, help_text='The highest number will be prioritized on multistack or single stack')),
                ('required_coupon', models.BooleanField(default=False, help_text='Set to True, To make use of coupons to apply')),
                ('start_date', models.DateTimeField(blank=True, help_text='Only valid on start of this date; To ignore if required_coupon is True', null=True)),
                ('end_date', models.DateTimeField(blank=True, help_text='Only valid on before end date; To ignore if required_coupon is True', null=True)),
                ('is_active', models.BooleanField(default=False, help_text='To quickly control whether this offer is still valid')),
                ('last_update_dt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='VendorShippingOptionSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_id', models.CharField(max_length=150)),
                ('tenant_id', models.CharField(max_length=150)),
                ('name', models.CharField(help_text='ex. Standard', max_length=255)),
                ('base_cost', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=15)),
                ('currency', models.CharField(default='SGD', help_text='Default currency specific to this Shipping option base cost or flat rate', max_length=50)),
                ('conditions', models.CharField(help_text='ex. { "max_weight": 30 }', max_length=150)),
                ('flat_rate', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=15)),
                ('delivery_time', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=False, help_text='To quickly control whether this option is still valid')),
                ('last_update_dt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerAddressSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.CharField(max_length=150)),
                ('address_type', models.CharField(choices=[('billing', 'Billing'), ('shipping', 'Shipping')], max_length=10)),
                ('street', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(blank=True, max_length=10, null=True)),
                ('postal', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=100)),
                ('is_default', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('last_update_dt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'unique_together': {('customer_id', 'address_type', 'is_default')},
            },
        ),
        migrations.CreateModel(
            name='UserAuthorizationSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=150)),
                ('permission_codename', models.CharField(max_length=255)),
                ('scope', models.CharField(help_text='ex. { "tenant_id": "t-1234" }', max_length=150)),
                ('is_active', models.BooleanField(default=True)),
                ('last_update_dt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'unique_together': {('user_id', 'permission_codename', 'scope')},
            },
        ),
        migrations.CreateModel(
            name='VendorProductSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=150)),
                ('vendor_id', models.CharField(max_length=150)),
                ('tenant_id', models.CharField(max_length=150)),
                ('product_sku', models.CharField(max_length=50)),
                ('product_name', models.CharField(max_length=255)),
                ('product_category', models.CharField(help_text='some countries uses category to calculate tax', max_length=100)),
                ('options', models.CharField(help_text='ex. {"Size": "M", "Color": "RED"}', max_length=150)),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.PositiveIntegerField()),
                ('product_currency', models.CharField(help_text='Currency for calculation requirements & validation. e.g. SGD', max_length=50)),
                ('package_weight', models.CharField(blank=True, help_text='value should be coming from product itself or to fill in later once it goes to warehouse fulfillment?', max_length=100, null=True)),
                ('package_length', models.CharField(blank=True, help_text='value should be coming from product itself or to fill in later once it goes to warehouse fulfillment? ', max_length=100, null=True)),
                ('package_width', models.CharField(blank=True, help_text='value should be coming from product itself or to fill in later once it goes to warehouse fulfillment?', max_length=100, null=True)),
                ('package_height', models.CharField(blank=True, help_text='value should be coming from product itself or to fill in later once it goes to warehouse fulfillment?', max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('last_update_dt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'unique_together': {('product_sku', 'vendor_id')},
            },
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_id', models.CharField(max_length=150)),
                ('vendor_name', models.CharField(help_text='can use to check if product belongs to same vendor', max_length=200)),
                ('vendor_country', models.CharField(help_text='can use to determine if shipping is domestic compared w shipping destination', max_length=200)),
                ('product_sku', models.CharField(max_length=50)),
                ('product_name', models.CharField(max_length=255)),
                ('product_category', models.CharField(help_text='some countries uses category to calculate tax', max_length=100)),
                ('is_free_gift', models.BooleanField(default=False)),
                ('is_taxable', models.BooleanField(default=True)),
                ('options', models.CharField(help_text='ex. {"Size": "M", "Color": "RED"}', max_length=150)),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_currency', models.CharField(help_text='Currency for calculation requirements & validation. e.g. SGD', max_length=50)),
                ('order_quantity', models.PositiveIntegerField(null=True)),
                ('package_weight', models.CharField(blank=True, help_text='value should be coming from product itself or to fill in later once it goes to warehouse fulfillment?', max_length=100, null=True)),
                ('package_length', models.CharField(blank=True, help_text='value should be coming from product itself or to fill in later once it goes to warehouse fulfillment? ', max_length=100, null=True)),
                ('package_width', models.CharField(blank=True, help_text='value should be coming from product itself or to fill in later once it goes to warehouse fulfillment?', max_length=100, null=True)),
                ('package_height', models.CharField(blank=True, help_text='value should be coming from product itself or to fill in later once it goes to warehouse fulfillment?', max_length=100, null=True)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, help_text='Total price w/o discounts; to apply discount per Order', max_digits=15, null=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='line_items', to='order_management.order')),
            ],
            options={
                'unique_together': {('product_sku', 'order')},
            },
        ),
    ]
