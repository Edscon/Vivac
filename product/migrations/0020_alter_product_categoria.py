# Generated by Django 4.1.4 on 2023-04-02 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0019_remove_category_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='categoria',
            field=models.ForeignKey(default='NONE', on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.category'),
        ),
    ]
