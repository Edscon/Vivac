# Generated by Django 4.1.7 on 2023-07-23 09:14

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0065_product_sexo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sexo',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('hombre', 'hombre'), ('mujer', 'mujer'), ('niño', 'niño'), ('niña', 'niña')], max_length=30, null=True),
        ),
    ]
