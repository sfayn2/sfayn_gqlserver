# Generated by Django 5.1.4 on 2025-01-29 23:54

import ddd.order_management.domain.enums
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0002_alter_order_final_amount_alter_order_payment_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='final_amount',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='overall total - discounts + ship cost + tax, etc. ?', max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_amount',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='amount paid by customer', max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(blank=True, choices=ddd.order_management.domain.enums.PaymentMethod.choices, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_cost',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_method',
            field=models.CharField(blank=True, choices=ddd.order_management.domain.enums.ShippingMethod.choices, help_text='i.e. Free Shipping, Local Pickup', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='tax_amount',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='tax amount', max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='overall total', max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_discounts_fee',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='total discounts fee per order', max_digits=15, null=True),
        ),
    ]
