# Generated by Django 4.2 on 2023-05-14 13:19

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('provider', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.IntegerField(blank=True, help_text='warehouse stocks ', null=True)),
                ('low_stock', models.IntegerField(blank=True, help_text='warehouse low stock to track inventory? ', null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=3, default=Decimal('0.0'), help_text='warehouse stock price', max_digits=15, null=True)),
                ('status', models.IntegerField(choices=[(0, 'In Stock'), (1, 'Out Of Stock'), (2, 'Low Stock')], null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2stock', to=settings.AUTH_USER_MODEL)),
                ('product_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prodvariant2stock', to='product.variantitem')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouse2stock', to='provider.provider')),
            ],
        ),
    ]
