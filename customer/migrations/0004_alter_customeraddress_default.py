# Generated by Django 3.2.4 on 2021-07-10 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20210622_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeraddress',
            name='default',
            field=models.BooleanField(default=False),
        ),
    ]
