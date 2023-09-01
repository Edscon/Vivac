from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .cart import Cart
from product.models import Product, Variant, Color



def add_to_cart(request, product_id, color, size):
    cart = Cart(request)
    size = size.replace('|', '/') # for sizes 40(2/3)
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
