import stripe
import json
import time
import os
import requests

from django.contrib.auth import login
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404

from cart.cart import Cart

from .models import Order, OrderItem, UserPayment, ClueInfo
from product.models import Product, Variant

# This is your test secret API key.
stripe.api_key = settings.STRIPE_API_KEY_HIDDEN

from flask import Flask, render_template, jsonify, request

app = Flask(__name__, static_folder='public',
            static_url_path='', template_folder='public')

def calculate_order_amount(items):
    price = int(items[1] * 100)
    return price

@csrf_exempt
def create_payment(request):
    try:
        cart = Cart(request)
        data = json.loads(request.body)

        if(data['customer'] == ''):
            customer = stripe.Customer.create(
                name = data['data']['first_name'] + ' ' + data['data']['last_name'],
                phone = data['data']['phone'],
                address={
                    'city': data['data']['city'],
                    'country': "ES",
                    'postal_code': data['data']['zipcode'],
                    'state': data['data']['provincia'],
                    'line1': data['data']['address'],
                },
                email=data['data']['email'],
            )
        else:
            #-----Modify customer-----
            customer = stripe.Customer.modify(
                data['customer'],
                name = data['data']['first_name'] + ' ' + data['data']['last_name'],
                phone = data['data']['phone'],
                address={
                    'city': data['data']['city'],
                    'country': "ES",
                    'postal_code': data['data']['zipcode'],
                    'state': data['data']['provincia'],
                    'line1': data['data']['address'],
                },
                email=data['data']['email'],
            )
        
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            customer=customer['id'],
            amount=calculate_order_amount(data['items']),
            currency='eur',
            # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
            automatic_payment_methods={
                'enabled': True,
            },
            payment_method_configuration= 'pmc_1NwVxXEUHJ3WTNbaat4t1kxi',
            metadata={"envio": data['data']['envio'], },
        )
        
        return JsonResponse({'clientSecret': intent['client_secret'], 'customer_id': intent['customer'] })
    except Exception as e:
        return jsonify(error=str(e)), 403
    
def success(request):
    cart = Cart(request)
    try:
        stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
        payment_intent = request.GET.get('payment_intent', None)
        client_secret = request.GET.get('payment_intent_client_secret', None)
        email = request.GET.get('email', None)

        payment_intent = stripe.PaymentIntent.retrieve(payment_intent)
        customer = stripe.Customer.retrieve(payment_intent.customer) 
        status = payment_intent.status

    except:
        customer = '0000000'

    '''ORDER'''
    order = []

    if(not Order.objects.filter(customer=customer.id)):
        
        if(email):
            user = User.objects.get(email=email)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        else: user = None

        order = Order.objects.create(
            user = user,
            customer = customer.id,
            first_name= customer.name.split(' ')[0],
            last_name = customer.name.split(' ')[1],
            email = customer.email,
            address = customer.address['line1'],
            zipcode = customer.address['postal_code'],
            city = customer.address['city'],
            provincia = customer.address['state'],
            phone = customer.phone,
            paid_amount = payment_intent.amount/100,
            envio = payment_intent.metadata.envio,
        )

    
        item_quant = {}
        variants = Variant.objects.filter(size__contains=['_']);
    
        for item in cart:
            variants2 = Variant.objects.filter(id=item['variant'].id)
            item_quant[item['variant'].id] = item['quantity']
            variants = variants | variants2
        
        for variant in variants:
            OrderItem.objects.create(
                order = order,
                variant = variant,
                nombre = variant.product.nombre,
                color = variant.color,
                size = variant.size.replace('/', '|'),
                precio = variant.precio,
                quantity = item_quant[variant.id],
                image_id = variant.image_id,
            )
        orden_compra = Order.objects.filter(customer = customer.id)[0]
        order =OrderItem.objects.filter(order=orden_compra )
        message_WhatsApp(customer, order,"%.2f" % round(payment_intent.amount/100, 2))
        
        cart.clear()
    

    orden_compra = Order.objects.filter(customer = customer.id)[0]
    order = OrderItem.objects.filter(order=orden_compra )
    subtotal = 0
    for i in order.values('precio'):
        subtotal = subtotal + i['precio']

    context = {
        'customer': customer,
        'order': order,
        'orden_compra': orden_compra,
        'subtotal': subtotal,
    }
    

    return render(request, 'cart/success.html', context)


def payment_canceled(request):
    return render(request, 'cart/payment_canceled.html')

def message_WhatsApp(customer, order, amount):

    text_items = ''
    for item in order:
        url = f'https://edscon.pythonanywhere.com/shop/{item.nombre.lower().replace(" ", "-")}'
        text_items = text_items + f'*🤜{item.nombre}*\n      Talla: {item.size}\n\n{url}\n\n'

    info = ClueInfo.objects.all()[0]
    id_tel = info.id_tel
    num_tel = info.num_tel
    token = info.token
    
    try:
        url = f'https://graph.facebook.com/v17.0/{id_tel}/messages'
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        data = { "messaging_product": "whatsapp", "recipient_type":"individual", "to": f"{num_tel}", "type": "text", "preview_url": True,
                "text": { 
                    "body": f"*Avís compra!!*\n{customer.name}\n\n{text_items}_{amount}€_",
                } }

        r = requests.post(url, headers=headers, json=data)
        print('Mensaje enviado', r)
        return r
    except:
        return 0


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

