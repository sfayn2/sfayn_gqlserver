# Generated by Django 4.2 on 2023-05-18 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0002_remove_variantitem_package_height_and_more'),
        ('vendor', '0001_initial'),
        ('shipping', '0002_remove_method_note_method_desc_method_max_days_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Packaging',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField(blank=True, help_text='product  weight', null=True)),
                ('package_length', models.FloatField(blank=True, help_text='package weight', null=True)),
                ('package_width', models.FloatField(blank=True, help_text='package width', null=True)),
                ('package_height', models.FloatField(blank=True, help_text='package height', null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user2packaging', to=settings.AUTH_USER_MODEL)),
                ('product_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prodvariant2packaging', to='product.variantitem')),
            ],
        ),
        migrations.RemoveField(
            model_name='method',
            name='cost',
        ),
        migrations.RemoveField(
            model_name='method',
            name='max_days',
        ),
        migrations.RemoveField(
            model_name='method',
            name='min_days',
        ),
        migrations.RemoveField(
            model_name='zone',
            name='shipping_method',
        ),
        migrations.AddField(
            model_name='method',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='category2method', to='product.category'),
        ),
        migrations.AddField(
            model_name='method',
            name='product_variant',
            field=models.ManyToManyField(blank=True, related_name='prodvariant2method', to='product.variantitem'),
        ),
        migrations.AddField(
            model_name='method',
            name='shipping_zone',
            field=models.ManyToManyField(blank=True, related_name='zone2method', to='shipping.zone'),
        ),
        migrations.AddField(
            model_name='method',
            name='tag',
            field=models.ManyToManyField(blank=True, related_name='tag2method', to='tag.tag'),
        ),
        migrations.AddField(
            model_name='method',
            name='vendor',
            field=models.ManyToManyField(blank=True, related_name='vendor2method', to='vendor.vendor'),
        ),
        migrations.RemoveField(
            model_name='method',
            name='classification',
        ),
        migrations.DeleteModel(
            name='Classification',
        ),
        migrations.AddField(
            model_name='method',
            name='classification',
            field=models.TextField(blank=True, help_text="ex. [{ 'name': '3 hours express', 'max_Weight_kg': 1, min_LWH_cm: 60, 'cost':  14 }, { 'name': 'Specific Delivery Slot', 'max_Weight_kg': 1, min_LWH_cm: 60, 'cost':  18 }, ]", null=True),
        ),
    ]
