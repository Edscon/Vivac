# Generated by Django 4.1.4 on 2023-08-22 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0072_variant_nombre'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='popular_rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
