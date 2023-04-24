# Generated by Django 4.2 on 2023-04-22 13:32

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
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='GST, VAT, ?', max_length=20)),
                ('country', models.CharField(max_length=50)),
                ('rate', models.FloatField(blank=True, help_text='N% tax rate per order?', null=True)),
                ('status', models.IntegerField(choices=[(0, 'Active'), (1, 'In Active')], null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2tax', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]