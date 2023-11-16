from django.db import models
from django.utils.safestring import mark_safe

class GastosProvincia(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.FloatField()

    class Meta:
        verbose_name_plural = 'Gastos_Provincia'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre