# Generated by Django 4.1.7 on 2023-07-15 16:43

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0059_product_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='desc',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]