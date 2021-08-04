# Generated by Django 3.2.4 on 2021-07-10 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_auto_20210710_0656'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productvariant',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='productvariant',
            name='parent_sn',
        ),
        migrations.AlterField(
            model_name='producttagitem',
            name='product_variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variant2tag', to='product.productvariantitem'),
        ),
        migrations.AlterField(
            model_name='productvariantitem',
            name='parent_sn',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product2variantitem', to='product.productparent'),
        ),
    ]