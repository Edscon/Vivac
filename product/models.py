from django.contrib.auth.models import User
from django.db import models
from django.core.files import File
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField
from multiselectfield import MultiSelectField

from io import BytesIO
from PIL import Image
from django.utils.translation import gettext_lazy as _

class Marca(models.Model):
    nombre = models.CharField(max_length=255)
    slug = models.SlugField()
    orden = models.IntegerField(default=0)
    sizes_shoes = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(
        upload_to='uploads/marcas/', blank=True, null=True)

    class Meta:
        verbose_name_plural = '3 - Marcas'
        ordering = ['orden']

    def __str__(self):
        return self.nombre

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="15" />'.format(self.image.url))
        else:
            return ""

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return 'https://via.placeholder.com/240x240.jpg'

class RedSocial(models.Model):
    nombre = models.CharField(max_length=255)
    slug = models.SlugField()
    orden = models.IntegerField(default=0)
    url_share= models.URLField(blank=True, null=True)
    image = models.ImageField(
        upload_to='uploads/RedSocial/', blank=True, null=True)

    class Meta:
        verbose_name_plural = '99 - Red Socials'
        ordering = ['orden']

    def __str__(self):
        return self.nombre

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="15" />'.format(self.image.url))
        else:
            return ""

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return 'https://via.placeholder.com/240x240.jpg'


class Category(models.Model):
    nombre = models.CharField(max_length=255)
    nombre_ca = models.CharField(max_length=255)
    slug = models.SlugField()
    orden = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to='uploads/categorias/', blank=True, null=True)

    class Meta:
        verbose_name_plural = '2 - Categories'
        ordering = ('orden',)

    def __str__(self):
        return self.nombre

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50" />'.format(self.image.url))
        else:
            return ""

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return 'https://via.placeholder.com/240x240.jpg'


class Product(models.Model):

    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),
    )
    TIPOS = (
        ('None', 'None'),
        ('Zapatos', 'Zapatos'),
        ('Ropa', 'Ropa'),
        ('Otros', 'Otros'),
    )
    SEXO = (
        ('hombre', 'hombre'),
        ('mujer', 'mujer'),
        ('nino', 'nino'),
        ('nina', 'nina'),
    )

    categoria = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    marca = models.ForeignKey(
        Marca, on_delete=models.CASCADE, null=True)
    tipo = models.CharField(
        max_length=10, choices=TIPOS, default='None')
    sexo = MultiSelectField(choices=SEXO, null=True, blank=True, max_length=30)
    nombre = models.CharField(max_length=255)
    nombre_ca = models.CharField(max_length=255)
    slug = models.SlugField()
    descripcion = RichTextField(blank=True, null=True)
    video = models.CharField(max_length=255, blank=True, null=True)
    precio_retail = models.FloatField(null=True)
    precio = models.FloatField()
    unidades = models.IntegerField(null=True)
    variants = models.CharField(
        max_length=10, choices=VARIANTS, default='None')
    creado_en = models.DateTimeField(auto_now_add=True)
    image_id = models.IntegerField(null=True) 
    sizes_shoes = models.CharField(max_length=255, blank=True, null=True)
    popular_rating = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = '1 - Products'
        ordering = ('-creado_en',)

    def __str__(self):
        return self.nombre

    def image(self):
        img = Image.objects.get(id = self.image_id)
        if img.id is not None:
            return img.image.url
        else:
            return 'https://via.placeholder.com/240x240.jpg'

    def image_tag(self):
        img = Image.objects.get(id=self.image_id)
        if img:
            return mark_safe('<img src="{}" height="50" />'.format(img.image.url))
        else:
            return ""

    def get_display_precio(self):
        return self.precio

    def get_descuento(self):
        if self.precio_retail:
            return round((self.precio_retail - self.precio)/self.precio_retail*100)
        else:
            return 0

    def get_ahorro(self):
        return (self.precio_retail - self.precio)

    def get_rating(self):
        reviews_total = 0

        for review in self.reviews.all():
            reviews_total += review.rating

        if reviews_total > 0:
            return reviews_total / self.reviews.count()

        return 0


class Image(models.Model):
    nombre = models.CharField(max_length=20, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/images', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnail/', blank=True, null=True)

    class Meta:
        verbose_name_plural = '5 - Images'

    def __str__(self):
        return self.nombre

    def ID(self):
            return self.id
        
    def image_tag(self):
        if self.image:
            return mark_safe('<img src="{}" height="200" />'.format(self.image.url))
        else:
            return ""

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x240.jpg'

    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

class Color(models.Model):
    nombre = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True)
    slug = models.SlugField()

    def __str__(self):
        return self.nombre

    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""

class Size(models.Model):
    nombre = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True)
    marca = models.ForeignKey(Marca, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class ExtraImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = color = models.ForeignKey(
        Color, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='uploads/imagesExtra', blank=True, null=True)
    
    def image_tag(self):
        if self.image:
            return mark_safe('<img src="{}" height="200" />'.format(self.image.url))
        else:
            return ""
        
    def ID(self):
            return self.id

class Variant(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(
        Color, on_delete=models.CASCADE, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    precio_retail = models.FloatField(null=True)
    precio = models.FloatField(default=0)
    unidades = models.IntegerField(default=1)
    image_id = models.IntegerField(null=True)

    def __str__(self):
        return self.nombre

    def image(self):
        img = Image.objects.get(id = self.image_id)
        if img.id is not None:
            return img.image.url
        else:
            return 'https://via.placeholder.com/240x240.jpg'

    def image_tag(self):
        img = Image.objects.get(id=self.image_id)
        if img:
            return mark_safe('<img src="{}" height="50" />'.format(img.image.url))
        else:
            return ""
        
    def get_display_precio(self):
        return self.precio

    def get_descuento(self):
        if self.precio_retail:
            return round((self.precio_retail - self.precio)/self.precio_retail*100)
        else:
            return 0

    def get_ahorro(self):
        return (self.precio_retail - self.precio)

    def get_nombre(self):
        return (self.nombre)


class Review(models.Model):
    product = models.ForeignKey(
        Product, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(default=3)
    titulo = models.TextField(default='', verbose_name=_('Título'))
    content = models.TextField()
    created_by = models.ForeignKey(
        User, related_name='reviews', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '4 - Reviews'
