# Generated by Django 4.2 on 2023-05-14 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0001_initial'),
        ('shipping', '0004_remove_method_desc_method_note_method_provider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='method',
            name='provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='provider2method', to='provider.provider'),
        ),
    ]
