# Generated by Django 4.1.7 on 2023-05-05 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0051_alter_product_tipo_extraimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extraimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/imagesExtra'),
        ),
    ]
