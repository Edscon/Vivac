# Generated by Django 4.1.7 on 2023-04-27 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0028_remove_variant_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variant',
            name='size',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Size',
        ),
    ]