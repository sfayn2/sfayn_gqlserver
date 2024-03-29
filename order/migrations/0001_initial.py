# Generated by Django 4.2 on 2023-06-03 12:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shipping', '0001_initial'),
        ('payment', '0001_initial'),
        ('tax', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('payment_method_name', models.CharField(blank=True, max_length=50, null=True)),
                ('tax_name', models.CharField(help_text='GST, VAT, ?', max_length=20)),
                ('tax_country', models.CharField(max_length=50)),
                ('subtotal', models.DecimalField(blank=True, decimal_places=3, help_text='total items w/o order discounts and tax', max_digits=15, null=True)),
                ('discounts_fee', models.DecimalField(blank=True, decimal_places=3, help_text='total discounts fee per order', max_digits=15, null=True)),
                ('discounted_subtotal', models.DecimalField(blank=True, decimal_places=3, help_text='subtotal minus discounts fee', max_digits=15, null=True)),
                ('tax_rate', models.DecimalField(blank=True, decimal_places=3, help_text='N% tax rate per order', max_digits=15, null=True)),
                ('tax_amount', models.DecimalField(blank=True, decimal_places=3, help_text='tax amount', max_digits=15, null=True)),
                ('shipping_fee', models.DecimalField(blank=True, decimal_places=3, help_text='shipping fee', max_digits=15, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=3, help_text='overall total', max_digits=15, null=True)),
                ('currency', models.TextField(blank=True, help_text='USD')),
                ('amount_paid', models.DecimalField(blank=True, decimal_places=3, help_text='amount paid by customer', max_digits=15, null=True)),
                ('customer_note', models.TextField(blank=True, help_text='Customer notes to seller')),
                ('status', models.IntegerField(blank=True, choices=[(0, 'Waiting For Payment'), (1, 'Paid'), (2, 'Processing'), (3, 'Partially Shipped Out'), (4, 'Shipped Out'), (5, 'Refunded'), (6, 'Cancel'), (7, 'Completed')], null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2order', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer2order', to=settings.AUTH_USER_MODEL)),
                ('payment_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment2order', to='payment.paymentmethod')),
                ('tax', models.ForeignKey(blank=True, help_text='Country tax applied', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tax2order', to='tax.tax')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('order_quantity', models.IntegerField(null=True)),
                ('product_sn', models.CharField(blank=True, max_length=25, null=True)),
                ('product_price', models.DecimalField(blank=True, decimal_places=3, help_text='undiscounted price', max_digits=15, null=True)),
                ('product_options', models.CharField(blank=True, max_length=50, null=True)),
                ('product_variant_name', models.CharField(blank=True, max_length=50, null=True)),
                ('product_img_upload', models.ImageField(blank=True, help_text='Primary img', null=True, upload_to=utils.path_and_rename)),
                ('product_img_url', models.CharField(blank=True, help_text='secondary img', max_length=300, null=True)),
                ('discounts_fee', models.DecimalField(blank=True, decimal_places=3, help_text='discounts per item', max_digits=15, null=True)),
                ('discounted_price', models.DecimalField(blank=True, decimal_places=3, help_text='(prince * qty) - dicount_fee', max_digits=15, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=3, help_text='can be discounted price or item original price?', max_digits=15, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2orderitem', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order2orderitem', to='order.order')),
                ('product_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prodvariant2orderitem', to='product.variantitem')),
            ],
        ),
        migrations.CreateModel(
            name='OrderFulfillment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_number', models.CharField(blank=True, help_text='a string fulfillment tracking number', max_length=120, null=True)),
                ('provider_id', models.IntegerField(blank=True, null=True)),
                ('provider_name', models.CharField(blank=True, max_length=20, null=True)),
                ('company_url', models.CharField(blank=True, max_length=200, null=True)),
                ('tracker_url', models.CharField(blank=True, max_length=200, null=True)),
                ('logo', models.ImageField(blank=True, help_text='company logo', null=True, upload_to=utils.path_and_rename)),
                ('shipping_method_name', models.CharField(blank=True, help_text='ex. Free shipping, Local pickup', max_length=50, null=True)),
                ('shipping_method_note', models.CharField(blank=True, help_text='ex. 2-3 days delivery', max_length=150, null=True)),
                ('shipping_method_cost', models.DecimalField(blank=True, decimal_places=3, help_text='overall total', max_digits=15, null=True)),
                ('shipping_address', models.TextField(blank=True)),
                ('shipping_postal', models.CharField(max_length=50)),
                ('shipping_country', models.CharField(max_length=50)),
                ('shipping_region', models.CharField(max_length=50)),
                ('status', models.IntegerField(blank=True, choices=[(0, 'Not Fulfilled'), (1, 'Fulfilled'), (2, 'Cancel')], null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2orderfulfillment', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order2orderfulfill', to='order.order')),
                ('order_item', models.ForeignKey(blank=True, help_text='Not applicable if all items has the same fulfillment', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orderitem2orderfulfill', to='order.orderitem')),
                ('shipping_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shipmethod2fulfillment', to='shipping.method')),
            ],
        ),
    ]
