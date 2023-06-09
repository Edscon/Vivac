# Generated by Django 4.1.4 on 2023-04-02 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0021_alter_product_categoria'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('orden', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/')),
            ],
            options={
                'ordering': ['orden'],
            },
        ),
    ]
