# Generated by Django 4.1.4 on 2022-12-26 00:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_product_precio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='url',
            new_name='slug',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='url',
            new_name='slug',
        ),
    ]
