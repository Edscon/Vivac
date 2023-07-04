import stripe
import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect

from cart.cart import Cart

from .models import Order, OrderItem


def start_order(request):

    cart = Cart(request)
    data = json.loads(request.body)
    total_price = 0
    
    items = []
    
    for item in cart:
        variant = item['variant']
        total_price += variant.precio * int(item['quantity'])
        
        nombre = variant.product.nombre + ' ' + variant.size + ' ' + variant.color.nombre

        items.append({
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': nombre,
                },
                'unit_amount': int(round(float(variant.precio) * 100, 2)),
            },
            'quantity': item['quantity'],
        })
        

    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items,
        mode='payment',
        success_url='http://127.0.0.1:8000/cart/success/',
        cancel_url='http://127.0.0.1:8000/cart/'
    )
    payment_intent = session.payment_intent

    order = Order.objects.create(
        user=request.user,
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        address=data['address'],
        zipcode=data['zipcode'],
        city=data['city'],
        provincia=data['provincia'],
        phone=data['phone'],
        paid=True,
        paid_amount=total_price,
    )
    order.payment_intent = payment_intent
    order.save()

    for item in cart:
        variant = item['variant']
        quantity = int(item['quantity'])
        price = variant.precio * quantity

        item = OrderItem.objects.create(
            order=order, variant=variant, price=price, quantity=quantity)

    cart.clear()

    return JsonResponse({'session': session, 'order': payment_intent})
