from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea, FileInput

from .models import Category, Product, Marca, Color, Size, Variant, Review, Image, ExtraImage, RedSocial


class MarcaOrderAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'orden', 'image_tag']
    prepopulated_fields = {'slug': ('nombre',)}

class RedSocialOrderAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'orden', 'image_tag']
    prepopulated_fields = {'slug': ('nombre',)}


class CategoryOrderAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'orden', 'image_tag']
    prepopulated_fields = {'slug': ('nombre',)}


class ProductVariantsInline(admin.TabularInline):
    model = Variant
    readonly_fields = ['image_tag']
    extra = 1
    show_change_link = True
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '10'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.FloatField: {'widget': TextInput(attrs={'size': '10'})},
        models.ImageField: {'widget': FileInput(attrs={'size': '10'})},
    }

class ProductImageInline(admin.TabularInline):
    model = Image
    readonly_fields = ['ID','image_tag']
    exclude = ['thumbnail']
    extra = 1
    show_change_link = True

class ProductExtraImagesInline(admin.TabularInline):
    model = ExtraImage
    readonly_fields = ['image_tag']
    extra = 10
    show_change_link = True

class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'image_tag']
    list_filter = ['categoria']
    inlines = [ProductImageInline, ProductVariantsInline, ProductExtraImagesInline]
    prepopulated_fields = {'slug': ('nombre',)}

class ColorOrderAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'code', 'color_tag']

class SizeOrderAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'code']

class VariantOrderAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'color', 'size',
                    'precio', 'image_tag']

class ImageOrderAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'id']
    readonly_fields = ['id','image_tag']

class ReviewOrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'created_by', 'rating', 'titulo',]
    list_filter = ['rating', 'created_at']
    search_fields = ['rating']


admin.site.register(Category, CategoryOrderAdmin)
admin.site.register(Product, ProductOrderAdmin)
admin.site.register(Marca, MarcaOrderAdmin)
admin.site.register(RedSocial, RedSocialOrderAdmin)
admin.site.register(Color, ColorOrderAdmin)
admin.site.register(Size, SizeOrderAdmin)
admin.site.register(Variant, VariantOrderAdmin)
admin.site.register(Review, ReviewOrderAdmin)
admin.site.register(Image, ImageOrderAdmin)