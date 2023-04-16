# Generated by Django 4.2 on 2023-04-16 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0025_remove_productparent_shop'),
        ('tag', '0002_remove_tag_discount_tag_img_upload_tag_img_url'),
        ('shop', '0011_remove_shopprofile_category_and_more'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('discount', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discount',
            name='discount_percentage',
        ),
        migrations.RemoveField(
            model_name='discount',
            name='discount_price',
        ),
        migrations.RemoveField(
            model_name='discount',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='discount',
            name='minimum_quantity',
        ),
        migrations.RemoveField(
            model_name='discount',
            name='start_date',
        ),
        migrations.AddField(
            model_name='discount',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='category2discount', to='product.productcategory'),
        ),
        migrations.AddField(
            model_name='discount',
            name='discount_type',
            field=models.ForeignKey(default=None, help_text='Select a discount rules for shop, tags, or any product variants', on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='discount',
            name='object_id',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='discount',
            name='product_variant',
            field=models.ManyToManyField(blank=True, related_name='prodvariant2discount', to='product.productvariantitem'),
        ),
        migrations.AddField(
            model_name='discount',
            name='shop',
            field=models.ManyToManyField(blank=True, related_name='shop2discount', to='shop.shopprofile'),
        ),
        migrations.AddField(
            model_name='discount',
            name='tag',
            field=models.ManyToManyField(blank=True, related_name='tag2discount', to='tag.tag'),
        ),
    ]
