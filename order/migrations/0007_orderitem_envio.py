# Generated by Django 4.1.4 on 2023-11-20 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_userpayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='envio',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
