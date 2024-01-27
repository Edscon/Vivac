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
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from email.mime.image import MIMEImage

from cart.cart import Cart
from cart.views import date_by_adding_business_days
from datetime import date

from .models import Order, OrderItem, UserPayment, ClueInfo
from product.models import Product, Variant, Image

# This is your test secret API key.
stripe.api_key = settings.STRIPE_API_KEY_HIDDEN

from flask import Flask, render_template, jsonify, request

app = Flask(__name__, static_folder='public',
            static_url_path='', template_folder='public')

def calculate_order_amount(cart):
    price = 0
    for item in cart:
        price = price + (item['total_price'] * 100)

    return int(price)

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
            amount=calculate_order_amount(cart),
            currency='eur',
            # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
            automatic_payment_methods={
                'enabled': True,
            },
            payment_method_configuration= 'pmc_1NwVxXEUHJ3WTNbaat4t1kxi',
            metadata={"envio": str(data['data']['envio']) + "|@|" + str(data['data']['detalles_envio'])},
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
            envio = int(payment_intent.metadata.envio.split('|@|')[0]),
            detalles_envio = payment_intent.metadata.envio.split('|@|')[1],
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
    order = OrderItem.objects.filter(order=orden_compra)
    subtotal = 0
    for i in order.values('precio'):
        subtotal = subtotal + i['precio']

    send_email_order(order, customer)
    time = date_by_adding_business_days(orden_compra.created_at, 1)

    context = {
        'customer': customer,
        'order': order,
        'orden_compra': orden_compra,
        'subtotal': subtotal,
        'time': time
    } 

    return render(request, 'cart/success.html', context)


def payment_canceled(request):
    return render(request, 'cart/payment_canceled.html')

def message_WhatsApp(customer, order, amount):
    
    text_items = ''
    for item in order:
        url = f'https://edscon.pythonanywhere.com/shop/{item.nombre.lower().replace(" ", "-")}'
        text_items = text_items + f'*🤜{item.nombre}*\n      Talla: {item.size}\n      Quantitat: {item.quantity}\n{url}\n\n'

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


def send_email_order(order, customer):
    
    name = customer.name
    email = order[0].order.email
    email = 'eduard.soler.11@gmail.com'
    
    content = 'Esports Vivac'

    from_email = settings.EMAIL_HOST_USER

    subtotal = 0
    for i in order.values('precio'):
        subtotal = subtotal + i['precio']

    time = date_by_adding_business_days(order[0].order.created_at, 1)

    html = render_to_string('core/emails/pedidoform.html', {'customer': customer, 'order_items': order, 'order': order[0].order, 'subtotal': subtotal, 'time': time})
        
    email_message = EmailMultiAlternatives(
        f'TU PEDIDO #{order[0].order.id} EN ESPORTS VIVAC HA SIDO CONFIRMADO',
        content,
        from_email,
        [email],
    )

    email_message.attach_alternative(html, "text/html")

    email_message.mixed_subtype = 'related'

    img_variants = {}
    for item in order:
        nombre = item.variant.id
        img = Image.objects.get(pk=item.variant.image_id)

        if nombre not in img_variants:
            img_variants[nombre] = img.image.url.split('images/')[1]

    for f in ['logo.png',]:
        fp = open(os.path.join(os.path.dirname(__file__), '..', 'static', 'img', f), 'rb')
        msg_img = MIMEImage(fp.read())
        fp.close()
        msg_img.add_header('Content-ID', '<{}>'.format(f))
        email_message.attach(msg_img)

    for name, url in img_variants.items():
        fp = open(os.path.join(os.path.dirname(__file__), '..', 'media', 'uploads', 'images', url), 'rb')
        msg_img = MIMEImage(fp.read())
        fp.close()
        msg_img.add_header('Content-ID', '<{}>'.format(name))
        email_message.attach(msg_img)

     
    email_message.send(fail_silently=False)

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