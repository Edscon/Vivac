# Generated by Django 4.1.7 on 2023-05-04 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0049_alter_category_options_alter_image_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tipo',
            field=models.CharField(choices=[('None', 'None'), ('Zapatos', 100), ('Ropa', 200), ('Otros', 300)], default='None', max_length=10),
        ),
    ]
