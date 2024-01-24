from itertools import product
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe

from product.models import Product, Variant, Color, Image

class Order(models.Model):

    SHIPPED = 'shipped'
    ORDERED = 'ordered'
    
    STATUS_CHOICES = (
        (ORDERED, 'Ordered'),
        (SHIPPED, 'Shipped')
    )

    user = models.ForeignKey(User, related_name='orders',blank=True, null=True , on_delete=models.CASCADE)
    customer = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    provincia = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    detalles_envio = models.TextField( blank=True, null=True)


    created_at = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)
    paid_amount = models.FloatField(blank=True, null=True) 
    envio = models.FloatField(blank=True, null=True)  

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED)

    class Meta:
        ordering = ('-created_at',)

    def get_total_price(self):
        if self.paid_amount:
            return self.paid_amount
        return 0
    

class OrderItem(models.Model):
    variant = models.ForeignKey(Variant, related_name='items', on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)

    nombre = models.CharField(max_length=255, blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    precio = models.FloatField(default=0)
    quantity = models.IntegerField(default=1)
    image_id = models.IntegerField(null=True)


    def get_total_price(self):
        return (self.precio)
    
    def image_tag(self):
        img = Image.objects.get(id=self.image_id)
        if img:
            return mark_safe('<img src="{}" height="200" />'.format(img.image.url))
        else:
            return ""

class ClueInfo(models.Model):
    token = models.CharField(max_length=250, blank=True, null=True)
    id_tel = models.CharField(max_length=250, blank=True, null=True)
    num_tel = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        verbose_name_plural = '1 - ClueInfo'

#----------------------------------------------------------------
class UserPayment(models.Model):
    app_user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=250)

@receiver(post_save, sender=User)
def create_user_payment(sender, instance, created, **kwargs):
    if created: 
        UserPayment.objects.create(app_user=instance)
        