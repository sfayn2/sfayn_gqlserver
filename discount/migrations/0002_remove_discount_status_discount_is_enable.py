# Generated by Django 4.2 on 2023-04-29 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discount',
            name='status',
        ),
        migrations.AddField(
            model_name='discount',
            name='is_enable',
            field=models.BooleanField(default=False),
        ),
    ]