# Generated by Django 4.1.7 on 2023-07-23 07:43

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0064_alter_product_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sexo',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Hombre', 'None'), ('Mujer', 'Zapatos'), ('Niño', 'Ropa'), ('Niña', 'Otros')], max_length=6, null=True),
        ),
    ]
