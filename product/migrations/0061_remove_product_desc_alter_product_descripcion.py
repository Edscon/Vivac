# Generated by Django 4.1.7 on 2023-07-15 16:44

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0060_product_desc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='desc',
        ),
        migrations.AlterField(
            model_name='product',
            name='descripcion',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
