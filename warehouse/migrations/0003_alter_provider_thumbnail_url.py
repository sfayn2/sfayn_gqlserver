# Generated by Django 4.2 on 2023-05-21 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0002_remove_stock_product_variant_stock_sku_provider_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='thumbnail_url',
            field=models.CharField(blank=True, help_text='thumbnail url', max_length=300, null=True),
        ),
    ]
