# Generated by Django 4.1.4 on 2023-12-03 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_account_favorites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='address',
        ),
        migrations.RemoveField(
            model_name='account',
            name='city',
        ),
        migrations.RemoveField(
            model_name='account',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='account',
            name='provincia',
        ),
        migrations.RemoveField(
            model_name='account',
            name='zipcode',
        ),
    ]
