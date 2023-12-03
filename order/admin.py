from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea, FileInput

from .models import Order, OrderItem, UserPayment, ClueInfo

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['nombre','color', 'size',
                    'precio','quantity', 'image_tag']


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['image_tag']
    exclude = ['image_id']
    extra = 0
    formfield_overrides = {
        models.ImageField: {'widget': FileInput(attrs={'size': '10'})},
    }

class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['first_name', 'address']
    inlines = [OrderItemInLine]

admin.site.register(ClueInfo)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(UserPayment)

