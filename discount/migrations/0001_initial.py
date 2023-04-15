# Generated by Django 4.2 on 2023-04-15 12:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=25)),
                ('minimum_quantity', models.IntegerField(null=True)),
                ('discount_price', models.FloatField(blank=True, help_text='Discount by Price', null=True)),
                ('discount_percentage', models.FloatField(blank=True, help_text='Discount by percentage', null=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('status', models.IntegerField(blank=True, choices=[(1, 'Enabled')], default=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2discount', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]