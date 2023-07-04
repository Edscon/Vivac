from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .cart import Cart
from product.models import Product, Variant, Color



def add_to_cart(request, product_id, color, size):
    print(color, size)
    cart = Cart(request)
    cart.add(product_id, color, size)
    
    response = render(request, 'cart/partials/menu_cart.html')
    
    response['HX-Trigger'] = 'update-menu-cart'

    return response

def cart(request):
    return render(request, 'cart/cart.html')


def success(request):
    return render(request, 'cart/success.html')


def update_cart(request, product_id, color, size, action):
    cart = Cart(request)
    
    if action == 'increment':
        cart.add(product_id, color, size, 1, True)
    else:
        cart.add(product_id, color, size, -1, True)

    variant = Variant.objects.get(product=Product.objects.get(id=product_id), color=Color.objects.get(code=color), size=size)
    variant_card = cart.get_item(variant.id)

    if variant_card:
        quantity = variant_card['quantity']
        item = {
            'variant': {
                'id': variant.id,
                'nombre': variant.nombre,
                'image': variant.image,
                'get_thumbnail': variant.image(),
                'price': variant.precio,
            },
            'total_price': float(quantity * variant.precio),
            'quantity': quantity,
        }
    else:
        item = None

    response = render(request, 'cart/partials/cart_item.html', {'item': item})

    response['HX-Trigger'] = 'update-menu-cart'

    return response


@login_required
def checkout(request):
    pub_key = settings.STRIPE_API_KEY_PUBLISHABLE
    return render(request, 'cart/checkout.html', {'pub_key': pub_key})


def hx_menu_cart(request):
    return render(request, 'cart/partials/menu_cart.html')

def hx_cart_total(request):
    return render(request, 'cart/partials/cart_total.html')

def hx_minicart(request):
    return render(request, 'cart/partials/minicart.html')
