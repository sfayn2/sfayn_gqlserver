# Generated by Django 5.1.4 on 2025-01-10 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_catalog', '0002_alter_product_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={},
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='package_height',
            field=models.CharField(blank=True, help_text='value can be estimated package weight or based on historic data?', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='package_length',
            field=models.CharField(blank=True, help_text='value can be estimated package weight or based on historic data?', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='package_weight',
            field=models.CharField(blank=True, help_text='value can be estimated package weight or based on historic data?', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='package_width',
            field=models.CharField(blank=True, help_text='value can be estimated package weight or based on historic data?', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='attributes',
            field=models.JSONField(blank=True, help_text='ex. {"other": "X", "Warranty": "1 year"}', null=True),
        ),
    ]
