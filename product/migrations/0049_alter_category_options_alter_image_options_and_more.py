# Generated by Django 4.1.7 on 2023-05-03 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0048_alter_image_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('orden',), 'verbose_name_plural': '2 - Categories'},
        ),
        migrations.AlterModelOptions(
            name='image',
            options={'verbose_name_plural': '5 - Images'},
        ),
        migrations.AlterModelOptions(
            name='marca',
            options={'ordering': ['orden'], 'verbose_name_plural': '3 - Marcas'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-creado_en',), 'verbose_name_plural': '1 - Products'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name_plural': '4 - Reviews'},
        ),
    ]
