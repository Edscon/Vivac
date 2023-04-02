from django.contrib.auth.models import User
from django.db import models
from django.core.files import File

from io import BytesIO
from PIL import Image

class Marca(models.Model):
    nombre = models.CharField(max_length=255)
    slug = models.SlugField()
    orden = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to='uploads/', blank=True, null=True)
    
    class Meta:
        ordering = ['orden']
    
    def __str__(self):
        return self.nombre

class Category(models.Model):
    nombre = models.CharField(max_length=255)
    slug = models.SlugField()
    image = models.ImageField(
        upload_to='uploads/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('nombre',)

    def __str__(self):
        return self.nombre

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return 'https://via.placeholder.com/240x240.jpg'


class Product(models.Model):
    categoria = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    slug = models.SlugField()
    descripcion = models.TextField(blank=True, null=True)
    precio = models.FloatField()
    creado_en = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

    class Meta:
        ordering = ('-creado_en',)

    def __str__(self):
        return self.nombre

    def get_display_precio(self):
        return self.precio

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

    def get_rating(self):
        reviews_total = 0

        for review in self.reviews.all():
            reviews_total += review.rating

        if reviews_total > 0:
            return reviews_total / self.reviews.count()

        return 0


class Review(models.Model):
    product = models.ForeignKey(
        Product, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(default=3)
    titulo = models.TextField(default='')
    content = models.TextField()
    created_by = models.ForeignKey(
        User, related_name='reviews', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
