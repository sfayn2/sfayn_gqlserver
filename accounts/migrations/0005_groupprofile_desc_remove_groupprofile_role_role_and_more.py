# Generated by Django 4.2 on 2023-04-24 01:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0004_groupprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupprofile',
            name='desc',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='groupprofile',
            name='role',
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='ex. VENDOR', max_length=20)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2role', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='groupprofile',
            name='role',
            field=models.ManyToManyField(related_name='role2group', to='accounts.role'),
        ),
    ]
