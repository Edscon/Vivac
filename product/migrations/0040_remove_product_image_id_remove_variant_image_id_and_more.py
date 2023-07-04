# Generated by Django 4.1.7 on 2023-05-03 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0039_remove_product_image_remove_product_thumbnail_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image_id',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='image_id',
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='product',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='variant',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/variants'),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]
