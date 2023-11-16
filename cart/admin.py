from django.contrib import admin

from .models import GastosProvincia

class GastosProvinciaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio']

admin.site.register(GastosProvincia, GastosProvinciaAdmin)