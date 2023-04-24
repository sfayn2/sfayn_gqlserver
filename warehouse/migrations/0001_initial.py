# Generated by Django 4.2 on 2023-04-24 06:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('postal', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('region', models.CharField(max_length=50)),
                ('handling_fee', models.FloatField(blank=True, help_text='Add handling fee per order', null=True)),
                ('status', models.IntegerField(choices=[(0, 'Active'), (1, 'In Active')], null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2warehouse', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.IntegerField(blank=True, help_text='warehouse stocks ', null=True)),
                ('price', models.FloatField(blank=True, help_text='warehouse pricing', null=True)),
                ('status', models.IntegerField(choices=[(0, 'In Stock'), (1, 'Out Of Stock')], null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2stock', to=settings.AUTH_USER_MODEL)),
                ('product_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_variant2stock', to='product.productvariantitem')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouse2stock', to='warehouse.warehouse')),
            ],
        ),
    ]
