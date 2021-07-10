# Generated by Django 3.2.4 on 2021-07-10 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_auto_20210710_1211'),
        ('shop', '0006_alter_shoporder_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopcart',
            name='product_variant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prodvariant2cart', to='product.productvariantitem'),
        ),
    ]
