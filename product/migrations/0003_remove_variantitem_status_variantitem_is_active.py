# Generated by Django 4.2 on 2023-04-29 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_variantitem_package_height_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variantitem',
            name='status',
        ),
        migrations.AddField(
            model_name='variantitem',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
