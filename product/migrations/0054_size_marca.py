# Generated by Django 4.1.4 on 2023-05-06 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0053_marca_sizes_shoes'),
    ]

    operations = [
        migrations.AddField(
            model_name='size',
            name='marca',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.marca'),
        ),
    ]
