# Generated by Django 4.1.4 on 2023-08-17 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0067_remove_extraimage_nombre_remove_variant_nombre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='extraimage',
            name='nombre',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='variant',
            name='nombre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]