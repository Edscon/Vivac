from itertools import product
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from product.models import Product, Variant

class Order(models.Model):

    SHIPPED = 'shipped'
    ORDERED = 'ordered'
    
    STATUS_CHOICES = (
        (ORDERED, 'Ordered'),
        (SHIPPED, 'Shipped')
    )

    user = models.ForeignKey(User, related_name='orders',blank=True, null=True , on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    provincia = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)
    paid_amount = models.FloatField(blank=True, null=True)   

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED)

    class Meta:
        ordering = ('-created_at',)

    def get_total_price(self):
        if self.paid_amount:
            return self.paid_amount
        return 0
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, related_name='items', on_delete=models.CASCADE, blank=True, null=True)
    price = models.FloatField()
    quantity = models.IntegerField(default=1)

    def get_total_price(self):
        return (self.price)


class UserPayment(models.Model):
    app_user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=250)

@receiver(post_save, sender=User)
def create_user_payment(sender, instance, created, **kwargs):
    if created: 
        UserPayment.objects.create(app_user=instance)
        