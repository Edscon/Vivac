# Generated by Django 4.1.4 on 2023-03-31 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_category_imagecategory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='imagecategory',
            new_name='image',
        ),
        migrations.AddField(
            model_name='category',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
