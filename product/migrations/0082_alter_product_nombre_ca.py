# Generated by Django 4.1.4 on 2024-03-27 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0081_product_nombre_ca'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='nombre_ca',
            field=models.CharField(max_length=255),
        ),
    ]
