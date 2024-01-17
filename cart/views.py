from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .cart import Cart
from .models import GastosProvincia
from product.models import Product, Variant, Color

import json
from datetime import datetime, date, timedelta


def add_to_cart(request, product_id, color, size):
    cart = Cart(request)
    size = size.replace('|', '/') # for sizes 40(2/3)
    cart.add(product_id, color, size)
    
    response = render(request, 'cart/partials/menu_cart.html')
    
    response['HX-Trigger'] = 'update-menu-cart'

    return response

#No considerar los fines de semana
def date_by_adding_business_days(from_date, add_days):
    if from_date.hour >= 13:
        add_days += 1
    business_days_to_add = add_days
    current_date = from_date
    while business_days_to_add > 0:
        current_date += timedelta(days=1)
        weekday = current_date.weekday()
        if weekday >= 5: # Sunday = 6
            continue
        business_days_to_add -= 1
    return current_date

def cart(request):
    time = date_by_adding_business_days(datetime.now(), 1)
    return render(request, 'cart/cart.html',{'time': time})


def update_cart(request, product_id, color, size, action):
    cart = Cart(request)
    size = size.replace('|', '/')
    if action == 'increment':
        cart.add(product_id, color, size, 1, True)
    elif action == 'decrement':
        cart.add(product_id, color, size, -1, True)
    
    variant = Variant.objects.get(product=Product.objects.get(pk=product_id), color=Color.objects.get(code=color), size=size)
    quantity = cart.get_item(variant.id)

    if action == 'remove':
        quantity = 0
        cart.remove(str(variant.id))

    size = size.replace('/', '|')
    if quantity:
        quantity = quantity['quantity']

        item = {
            'variant': {
                'id': variant.id,
                'nombre': variant.product.nombre,
                'image': variant.image,
                'get_thumbnail': variant.image(),
                'price': variant.precio,
                'product': variant.product,
                'precio_retail': variant.precio_retail,
                'get_descuento': variant.get_descuento,
                'color': {
                    'slug': Color.objects.get(code=color).slug
                }
            },
            'total_price': float(quantity * variant.precio),
            'quantity': quantity,
            'size': size,
            'color': color,
        }
    else:
        item = None

    time = date_by_adding_business_days(datetime.now(), 1)
    
    response = render(request, 'cart/partials/cart_item.html', {'item': item, 'time': time})

    response['HX-Trigger'] = 'update-menu-cart'

    return response


def checkout(request):
    pub_key = settings.STRIPE_API_KEY_PUBLISHABLE

    envios = {}
    gastos_provincia = GastosProvincia.objects.values('nombre')
    for i in range(0, len(gastos_provincia)):
        envios[GastosProvincia.objects.values('nombre')[i]['nombre']] = GastosProvincia.objects.values('precio')[i]['precio']
    
    return render(request, 'cart/checkout.html', {'pub_key': pub_key, 'envios': envios})
    

@csrf_exempt
def change_cart(request):
    cart = Cart(request)
    data = json.loads(request.body)
    
    products = []
    
    for item in cart:
        print(item)
        if(item['variant'].unidades < item['quantity']): 
            print('Cantidad Diferente')
            item['id'] = item['variant'].product.id
            products.append(item)
        item['variant'] = 0

    for item in products:
        print(item['quantity'])
        cart.add(item['id'], item['color'], item['size'].replace('|', '/'), 1, True)

    return JsonResponse({})


def hx_menu_cart(request):
    return render(request, 'cart/partials/menu_cart.html')

def hx_cart_total(request):
    return render(request, 'cart/partials/cart_total.html')

def hx_minicart(request):
    return render(request, 'cart/partials/minicart.html')

def hx_addtocart(request):
    return render(request, 'cart/partials/addtocart.html')

def hx_minicart_icon_num(request):
    return render(request, 'cart/partials/minicart_icon_num.html')
