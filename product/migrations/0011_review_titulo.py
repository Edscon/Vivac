# Generated by Django 4.1.7 on 2023-03-15 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_remove_review_titulo'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='titulo',
            field=models.TextField(default=''),
        ),
    ]