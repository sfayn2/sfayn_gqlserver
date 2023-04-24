# Generated by Django 4.2 on 2023-04-24 11:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('level', models.IntegerField(choices=[(1, 'Level 1'), (2, 'Level 2'), (3, 'Level 3')], null=True)),
                ('img_upload', models.ImageField(blank=True, help_text='Primary img', null=True, upload_to=utils.utils.path_and_rename)),
                ('img_url', models.CharField(blank=True, help_text='secondary img', max_length=300, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2category', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_sn', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=100, null=True)),
                ('goods_brand', models.CharField(blank=True, max_length=30, null=True)),
                ('goods_desc', models.TextField(null=True)),
                ('status', models.IntegerField(choices=[(0, 'Pending Review'), (1, 'Approved'), (2, 'Rejected')], null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cat2product', to='product.category')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2product', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2variant', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VariantItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sku', models.CharField(max_length=50)),
                ('quantity', models.IntegerField(blank=True, help_text='allocated or reserved quantity', null=True)),
                ('price', models.FloatField(blank=True, help_text='sale price, exclusive of tax', null=True)),
                ('options', models.CharField(blank=True, max_length=50, null=True)),
                ('img_upload', models.ImageField(blank=True, help_text='Primary img', null=True, upload_to=utils.utils.path_and_rename)),
                ('img_url', models.CharField(blank=True, help_text='secondary img', max_length=300, null=True)),
                ('default', models.BooleanField(default=False, help_text='default to display in product details page of similar product')),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=0, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2variantsitem', to=settings.AUTH_USER_MODEL)),
                ('product_sn', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product2variantitem', to='product.product')),
                ('product_variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variant2item', to='product.variant')),
            ],
        ),
    ]
