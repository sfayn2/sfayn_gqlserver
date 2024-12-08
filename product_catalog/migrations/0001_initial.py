# Generated by Django 5.1.4 on 2024-12-06 13:03

import django.db.models.deletion
import utils
import uuid
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('img_upload', models.ImageField(blank=True, help_text='Primary img', null=True, upload_to=utils.path_and_rename)),
                ('level', models.IntegerField(choices=[('level_1', 'Level 1'), ('level_2', 'Level 2'), ('level_3', 'Level 3')], null=True)),
                ('created_by', models.CharField(max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='product_catalog.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[('draft', 'Draft'), ('pending_review', 'Pending Review'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('deactivated', 'Deactivated')], default='draft', null=True)),
                ('created_by', models.CharField(max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cat2product', to='product_catalog.category')),
            ],
        ),
        migrations.CreateModel(
            name='VariantItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sku', models.CharField(max_length=50)),
                ('price', models.DecimalField(blank=True, decimal_places=3, default=Decimal('0.0'), help_text='sale price, exclusive of tax', max_digits=15, null=True)),
                ('options', models.CharField(blank=True, max_length=50, null=True)),
                ('img_upload', models.ImageField(blank=True, help_text='Primary img', null=True, upload_to=utils.path_and_rename)),
                ('default', models.BooleanField(default=False, help_text='default to display in product details page of similar product')),
                ('is_active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product2variantitem', to='product_catalog.product')),
                ('product_variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variant2item', to='product_catalog.variant')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('created_by', models.CharField(max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('product_variant', models.ManyToManyField(blank=True, related_name='prodvariant2tag', to='product_catalog.variantitem')),
            ],
        ),
    ]
