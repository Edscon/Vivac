# Generated by Django 4.1.7 on 2023-07-15 17:02

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0063_alter_product_descripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='descripcion',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]