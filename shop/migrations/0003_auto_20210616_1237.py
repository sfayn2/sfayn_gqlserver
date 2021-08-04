# Generated by Django 2.2.17 on 2021-06-16 12:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0001_initial'),
        ('payment', '0001_initial'),
        ('shop', '0002_auto_20210613_0658'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopOrder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('total_amount', models.FloatField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[(0, 'Waiting for Payment'), (1, 'Paid'), (2, 'Processing'), (3, 'Shipped Out'), (4, 'Refunded'), (5, 'Cancel'), (6, 'Completed')], max_length=50, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2order', to=settings.AUTH_USER_MODEL)),
                ('customer_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer2order', to='customer.CustomerAddress')),
                ('payment_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment2order', to='payment.PaymentMethod')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='shopcart',
            unique_together=set(),
        ),
        migrations.CreateModel(
            name='ShopOrderItems',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2orderitems', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order2orderitems', to='shop.ShopOrder')),
                ('shopcart', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart2orderitems', to='shop.ShopCart')),
            ],
        ),
    ]