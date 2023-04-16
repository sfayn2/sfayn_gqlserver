# Generated by Django 4.2 on 2023-04-16 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotional', '0002_promotionalbanner_display_order'),
        ('product', '0025_remove_productparent_shop'),
        ('shop', '0009_shopprofile_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopprofile',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, related_name='category2shop', to='product.productcategory'),
        ),
        migrations.AddField(
            model_name='shopprofile',
            name='promotional_banner',
            field=models.ManyToManyField(blank=True, null=True, related_name='banner2shop', to='promotional.promotionalbanner'),
        ),
        migrations.AlterField(
            model_name='shopprofile',
            name='product',
            field=models.ManyToManyField(blank=True, null=True, related_name='prod2shop', to='product.productparent'),
        ),
    ]