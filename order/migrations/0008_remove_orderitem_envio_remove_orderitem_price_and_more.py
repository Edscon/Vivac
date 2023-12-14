# Generated by Django 4.1.4 on 2023-11-20 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0075_product_popular_rating'),
        ('order', '0007_orderitem_envio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='envio',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='price',
        ),
        migrations.AddField(
            model_name='order',
            name='envio',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.color'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='image_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='nombre',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='precio',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='size',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]