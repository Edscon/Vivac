# Generated by Django 4.1.4 on 2024-03-27 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0080_alter_category_nombre_ca'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='nombre_ca',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]