# Generated by Django 4.1.7 on 2023-03-02 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_rename_titol_review_titulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='titulo',
            field=models.TextField(default=''),
        ),
    ]
