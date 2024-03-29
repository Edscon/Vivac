# Generated by Django 4.1.4 on 2024-02-02 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_account_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alquiler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('esquí_completo_adulto', models.FloatField()),
                ('snowblade_completo', models.FloatField()),
                ('snowboard_completo_adulto', models.FloatField()),
                ('esquí_gama_alta_completo_adulto', models.FloatField()),
                ('casco', models.FloatField()),
                ('esquí_completo_junior', models.FloatField()),
                ('snowboard_completo_junior', models.FloatField()),
                ('esquí_montaña_completo', models.FloatField()),
                ('raquetas', models.FloatField()),
                ('raquetas_y_palos', models.FloatField()),
                ('grampones', models.FloatField()),
                ('piolet', models.FloatField()),
                ('grampones_y_piolet', models.FloatField()),
                ('palos', models.FloatField()),
                ('esquí_temporada_adulto', models.FloatField()),
                ('esquí_temporada_junior_70_90cm', models.FloatField()),
                ('esquí_temporada_junior_100_110cm', models.FloatField()),
                ('esquí_temporada_junior_120_130cm', models.FloatField()),
                ('esquí_temporada_junior_140_150cm', models.FloatField()),
            ],
            options={
                'verbose_name_plural': '1 - Alquiler Material',
            },
        ),
    ]
