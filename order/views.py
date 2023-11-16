import stripe
import json
import time

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect

from cart.cart import Cart

from .models import Order, OrderItem, UserPayment


def start_order(request):

    cart = Cart(request)
    user_id = json.loads(request.body)
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
        customer_creation = 'always',
        success_url='http://127.0.0.1:8000/cart/success?session_id={CHECKOUT_SESSION_ID}'+ f'&pk={user_id}',
        cancel_url='http://127.0.0.1:8000/cart/payment_canceled',
        customer_email = "example@example.com",
    )
    payment_intent = session.payment_intent
    session['customer_details']['name'] = 'data["first_name"]'

    return JsonResponse({'session': session, 'order': payment_intent})


def success(request):
    cart = Cart(request)
    cart.clear()
    try:
        stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
        checkout_session_id = request.GET.get('session_id', None)
        session = stripe.checkout.Session.retrieve(checkout_session_id)
        customer = stripe.Customer.retrieve(session.customer)
        user_id = request.GET.get('pk', None)
        user_payment = UserPayment.objects.get(app_user = user_id)
        user_payment.stripe_checkout_id = checkout_session_id
        user_payment.save()
    except:
        customer = '0000000'
    '''ORDER'''


    return render(request, 'cart/success.html', {'customer': customer})

def payment_canceled(request):
    return render(request, 'cart/payment_canceled.html')

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
    time.sleep(10)
    payload = request.body
    signature_harder = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_harder, settings.STRIPE_WEBHOOK_SECRET_TEST
        )
    except ValueError as e:
        return HttpResponse(status = 400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status = 400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)
        user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
        line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
        user_payment.payment_bool = True
        user_payment.save()
    return HttpResponse(status = 200)

import os
import stripe

# This is your test secret API key.
stripe.api_key = settings.STRIPE_API_KEY_HIDDEN

from flask import Flask, render_template, jsonify, request

app = Flask(__name__, static_folder='public',
            static_url_path='', template_folder='public')

def calculate_order_amount(items):

    price = items[1] * 100
    return price

def create_payment(request):
    try:
        data = json.loads(request.body)

        # Create a PaymentIntent with the order amount and currency

        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data['items']),
            currency='eur',
            # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
            automatic_payment_methods={
                'enabled': True,
            },
            metadata={"order_id": "6735"},
        )
        return JsonResponse({'clientSecret': intent['client_secret']})
    except Exception as e:
        return jsonify(error=str(e)), 403
