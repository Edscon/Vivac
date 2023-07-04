from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Case, When
import json
import pandas as pd
import time

from .models import Product, Marca, Review, Variant, Color, Size, Image, ExtraImage

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
   
    products_list = Product.objects.all()[0:8]
    
    images_extra = ExtraImage.objects.filter(product=product, color=Variant.objects.filter(product=product).first().color)
    if images_extra.count() == 0: images_extra = ExtraImage.objects.filter(product=product)
    

    variants = Variant.objects.filter(product=product)
    colors =  unique(list(variants.values('color')),'color')
    
    size = unique(list(Variant.objects.filter(product=product, color=colors[0]).values('size')),'size')
    sizes = list(product.sizes_shoes.split(", "))

    lista = []
    for i in range(0,len(colors)):
            lista.append(Variant.objects.filter(color=colors[i]).first().id)
    
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(lista)])
    variant_colors = Variant.objects.filter(id__in=lista).order_by(preserved)

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
    
    context = {
        'product': product,
        'products_list': products_list,
        'variants': variants,
        'variant_colors': variant_colors,
        'colors': colors,
        'color_first': colors[0],
        'size': size,
        'sizes': sizes,
        'variant_url': False,
        'images_extra': images_extra,
    }
    return render(request, 'product/product.html', context)



def variant_product(request, slug, slug_color):

    products_list = Product.objects.all()[0:8]
    product = get_object_or_404(Product, slug=slug)

    color = get_object_or_404(Color, slug=slug_color)
    images_extra = ExtraImage.objects.filter(product=product, color=color)
    variant = Variant.objects.filter(product=product, color=color)

    variants = Variant.objects.filter(product=product)
    colors =  unique(list(variants.values('color')),'color')

    size = unique(list(Variant.objects.filter(product=product, color=color).values('size')),'size')
    sizes = list(product.sizes_shoes.split(", "))

    lista = []
    for i in range(0,len(colors)):
            lista.append(Variant.objects.filter(color=colors[i]).first().id)
    
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(lista)])
    variant_colors = Variant.objects.filter(id__in=lista).order_by(preserved)

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
        'variant_url': True,
        'images_extra': images_extra,
    }

    return render(request, 'product/variant.html', context)



def marca(request, slug):
    marca = get_object_or_404(Marca, slug=slug)

    return render(request, 'product/marca.html', {'marca': marca})


def marcas(request):

    marcas = Marca.objects.all()
    return render(request, 'product/marca.html', {'marcas': marcas})