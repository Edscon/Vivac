from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User, related_name='accounts', on_delete=models.CASCADE)
    address = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    zipcode = models.CharField(max_length=250, blank=True, null=True)
    phone = models.CharField(max_length=250, blank=True, null=True)
    provincia = models.CharField(max_length=250, blank=True, null=True)
    favorites = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Alquiler(models.Model):
    esquí_completo_adulto = models.FloatField()
    snowblade_completo = models.FloatField()
    snowboard_completo_adulto = models.FloatField()
    esquí_gama_alta_completo_adulto = models.FloatField()

    casco = models.FloatField()

    esquí_completo_junior = models.FloatField()
    snowboard_completo_junior = models.FloatField()

    esquí_montaña_completo = models.FloatField()
    raquetas = models.FloatField()
    raquetas_y_palos = models.FloatField()
    grampones = models.FloatField()
    piolet = models.FloatField()
    grampones_y_piolet = models.FloatField()

    palos = models.FloatField()

    esquí_temporada_adulto = models.FloatField()
    esquí_temporada_junior_70_90cm = models.FloatField()
    esquí_temporada_junior_100_110cm = models.FloatField()
    esquí_temporada_junior_120_130cm = models.FloatField()
    esquí_temporada_junior_140_150cm = models.FloatField()

    class Meta:
        verbose_name_plural = '1 - Alquiler Material'


