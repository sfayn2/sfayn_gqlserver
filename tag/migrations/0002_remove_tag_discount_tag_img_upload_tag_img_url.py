# Generated by Django 4.2 on 2023-04-16 06:28

from django.db import migrations, models
import utils.utils


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='discount',
        ),
        migrations.AddField(
            model_name='tag',
            name='img_upload',
            field=models.ImageField(blank=True, help_text='Primary img', null=True, upload_to=utils.utils.path_and_rename),
        ),
        migrations.AddField(
            model_name='tag',
            name='img_url',
            field=models.CharField(blank=True, help_text='secondary img', max_length=300, null=True),
        ),
    ]
