# Generated by Django 4.1.4 on 2023-03-31 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_rename_thumbnail_category_image_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='image_size',
        ),
    ]
