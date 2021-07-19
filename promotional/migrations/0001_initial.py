# Generated by Django 3.2.4 on 2021-07-19 12:26

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
            name='PromotionalBanner',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('img_upload', models.ImageField(blank=True, help_text='Primary img', null=True, upload_to=utils.utils.path_and_rename)),
                ('img_url', models.CharField(blank=True, help_text='secondary img', max_length=300, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2banner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
