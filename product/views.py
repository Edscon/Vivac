from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Case, When
import json
import pandas as pd
import time

from .models import Product, Marca, Review, Variant, Color, Size, Image, ExtraImage, RedSocial
from core.models import Account

def unique(lista,str):
    lista1 = []
    for i in range(0,len(lista)):
        lista1.append(lista[i][str])

    if str == 'color':
        lista1 = pd.unique(lista1)
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(lista1)])
        unicos = Color.objects.filter(id__in=lista1).order_by(preserved)
    if str == 'size':
        unicos = lista1
    return unicos
    

def product(request, slug):
    
    product = get_object_or_404(Product, slug=slug)
   
    products_list = Product.objects.filter(categoria=product.categoria).order_by('popular_rating')[0:8]
    
    images_extra = ExtraImage.objects.filter(product=product, color=Variant.objects.filter(product=product).first().color)
    if images_extra.count() == 0: images_extra = ExtraImage.objects.filter(product=product)
    

    variants = Variant.objects.filter(product=product)
    colors =  unique(list(variants.values('color')),'color')
    
    size = unique(list(Variant.objects.filter(product=product, color=colors[0]).values('size')),'size')
    sizes = list(product.sizes_shoes.split(", "))
    
    size_special = []

    for i in size:
        size_special.append(i.replace('/', '|'))


    lista = []
    for i in range(0,len(colors)):
            lista.append(Variant.objects.filter(color=colors[i], product=product).first().id)
    
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(lista)])
    variant_colors = Variant.objects.filter(id__in=lista).order_by(preserved)

    if request.user.is_authenticated:
        review_user = Review.objects.filter(
                    created_by=request.user, product=product).count()
    else: review_user = 0

    if request.method == 'POST':
        data = json.loads(request.body)
        rating = int(data['rating'])
        titulo = data['titulo']
        content = data['content']

        if content:
            reviews = Review.objects.filter(
                created_by=request.user, product=product)

            if reviews.count() > 0:
                review = reviews.first()
                if rating == 0:
                    rating = review.rating
                review.rating = rating
                review.titulo = titulo
                review.content = content

                review.save()

            else:
                review = Review.objects.create(
                    product=product,
                    rating=rating,
                    titulo=titulo,
                    content=content,
                    created_by=request.user,
                )
            return redirect('product', slug=slug)
    
    RedSocials = RedSocial.objects.all()

    favorite = False

    if(request.user.is_authenticated):
        if(Account.objects.filter(user = request.user).exists()):
            if(Account.objects.filter(user = request.user).values('favorites')[0]['favorites']):
                for i in Account.objects.filter(user = request.user).values('favorites')[0]['favorites'].split(','):
                    if(i == f'({product.id}/{colors[0].code})'):
                        favorite = True
    
    dic_sizes_precio = []
    for variant in variants:
        if (variant.size in size):
            dic_sizes_precio.append([variant.precio_retail, variant.precio, 
                                     variant.precio_retail - variant.precio, 
                                     variant.size, 
                                     round((variant.precio_retail - variant.precio)/variant.precio_retail*100)])
            
    context = {
        'product': product,
        'products_list': products_list,
        'variants': variants,
        'variant_colors': variant_colors,
        'colors': colors,
        'color_first': colors[0],
        'size': size,
        'sizes': sizes,
        'slug_color': variant_colors[0].color.slug,
        'size_special': size_special,
        'variant_url': False,
        'images_extra': images_extra,
        'RedSocials': RedSocials,
        'review_user': review_user,
        'favorite': favorite,
        'dic_sizes_precio': dic_sizes_precio
    }
    return render(request, 'product/product.html', context)



def variant_product(request, slug, slug_color):

    product = get_object_or_404(Product, slug=slug)
    
    products_list = Product.objects.filter(categoria=product.categoria).order_by('popular_rating')[0:8]

    color = get_object_or_404(Color, slug=slug_color)
    images_extra = ExtraImage.objects.filter(product=product, color=color)
    variant = Variant.objects.filter(product=product, color=color)

    variants = Variant.objects.filter(product=product)
    colors =  unique(list(variants.values('color')),'color')

    size = unique(list(Variant.objects.filter(product=product, color=color).values('size')),'size')
    sizes = list(product.sizes_shoes.split(", "))

    size_special = []

    for i in size:
        size_special.append(i.replace('/', '|'))

    lista = []
    for i in range(0,len(colors)):
            lista.append(Variant.objects.filter(color=colors[i]).first().id)
    
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(lista)])
    variant_colors = Variant.objects.filter(id__in=lista).order_by(preserved)

    if request.user.is_authenticated:
        review_user = Review.objects.filter(
                    created_by=request.user, product=product).count()
    else: review_user = 0

    if request.method == 'POST':
        data = json.loads(request.body)
        rating = int(data['rating'])
        titulo = data['titulo']
        content = data['content']

        if content:
            reviews = Review.objects.filter(
                created_by=request.user, product=product)

            if reviews.count() > 0:
                review = reviews.first()
                if rating == 0:
                    rating = review.rating
                review.rating = rating
                review.titulo = titulo
                review.content = content

                review.save()

            else:
                review = Review.objects.create(
                    product=product,
                    rating=rating,
                    titulo=titulo,
                    content=content,
                    created_by=request.user,
                )
            return redirect('product', slug=slug)

    RedSocials = RedSocial.objects.all()

    favorite = False

    if(request.user.is_authenticated):
        if(Account.objects.filter(user = request.user).exists()):
            if(Account.objects.filter(user = request.user).values('favorites')[0]['favorites']):
                for i in Account.objects.filter(user = request.user).values('favorites')[0]['favorites'].split(','):
                    if(i == f'({product.id}/{color.code})'):
                        favorite = True



    dic_sizes_precio = []
    for var in variants:
        if (var.size in size):
            dic_sizes_precio.append([var.precio_retail, var.precio, 
                                     var.precio_retail - var.precio, 
                                     var.size, 
                                     round((var.precio_retail - var.precio)/var.precio_retail*100)])
            
    context = {
        'product': product,
        'products_list': products_list,
        'variants': variant,
        'variants_first': variant[0],
        'variant_colors': variant_colors,
        'color': color,
        'size': size,
        'sizes': sizes,
        'slug_color': slug_color,
        'size_special': size_special,
        'variant_url': True,
        'images_extra': images_extra,
        'RedSocials': RedSocials,
        'favorite': favorite,
        'review_user': review_user,
        'dic_sizes_precio': dic_sizes_precio
    }

    return render(request, 'product/variant.html', context)



def marca(request, slug):
    marca = get_object_or_404(Marca, slug=slug)

    return render(request, 'product/marca.html', {'marca': marca})


def marcas(request):
    marcas = Marca.objects.all()

    return render(request, 'product/marca.html', {'marcas': marcas})