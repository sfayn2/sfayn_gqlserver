# Generated by Django 4.2 on 2023-04-23 13:09

from django.conf import settings
import django.contrib.sites.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('site_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sites.site')),
                ('weight_unit', models.CharField(help_text='all products weight unit will be default in {weight_unit}', max_length=5, null=True)),
                ('dimensions_unit', models.CharField(help_text='all products weight unit will be default in {dimensions_unit}', max_length=5, null=True)),
                ('product_approval', models.IntegerField(choices=[(0, 'Pending Review'), (1, 'Approved'), (2, 'Rejected')], default=1, help_text='when product is created it requires approval before it can be published?')),
                ('currency', models.CharField(help_text='USD, SGD, ..', max_length=10)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2settings', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('sites.site',),
            managers=[
                ('objects', django.contrib.sites.models.SiteManager()),
            ],
        ),
    ]
