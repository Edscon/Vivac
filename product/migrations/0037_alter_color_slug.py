# Generated by Django 4.1.4 on 2023-05-02 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0036_color_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='slug',
            field=models.SlugField(),
        ),
    ]