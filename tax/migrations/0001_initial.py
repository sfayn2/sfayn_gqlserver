# Generated by Django 4.2 on 2023-05-14 13:22

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
                ('region', models.CharField(blank=True, max_length=50, null=True)),
                ('rate', models.DecimalField(blank=True, decimal_places=3, help_text='N% tax rate', max_digits=15, null=True, verbose_name='Rate(%)')),
                ('is_active', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2tax', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
