# Generated by Django 4.1.4 on 2023-08-17 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0070_remove_image_nombre'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='nombre',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
