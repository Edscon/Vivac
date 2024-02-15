from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Case, When
from django.db.models import Min, Max
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from core.models import Account, Alquiler
from order.models import Order
from product.models import Product, Category, Marca, Variant, Color, Review
from functools import reduce
from itertools import chain
from cart.cart import Cart
from cart.views import date_by_adding_business_days
import json
import pandas as pd
import math

from .forms import SignUpForm


def login_p(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if(User.objects.filter(email = email ).count() > 0):
            user = User.objects.get(email = email)
            if (user.check_password(password)):
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                
            else:
                print('NO')
        else: 
            print('No existe usuario')

    return redirect(request.GET.get('next',''))

def frontpage(request):
    products = Product.objects.all()[0:8]
    categories = Category.objects.all()[0:4]
    marcas = Marca.objects.all()

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
    else:
        form = SignUpForm()

    
    lista = []
    if(request.user.is_authenticated):
        if(Account.objects.filter(user = request.user).exists()):
            if(Account.objects.filter(user = request.user).values('favorites')[0]['favorites']):
                for i in Account.objects.filter(user = request.user).values('favorites')[0]['favorites'].split(','):
                    id_col = i.replace('(', '').replace(')', '').split('/')
                    try:
                        lista.append(Variant.objects.filter(product = Product.objects.filter(id=int(id_col[0]))[0], color = Color.objects.filter(code = id_col[1])[0])[0].id)
                    except:
                        i = 0
        
    favorites = Variant.objects.filter(id__in = lista)
    
    context = {
        'products': products,
        'categories': categories,
        'marcas': marcas,
        'favorites': favorites,
    }

    return render(request, 'core/frontpage.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
    else:
        form = SignUpForm()

    return render(request, 'core/signup.html', {'form': form})


def create_account(user, data):
    account = Account(
        user = user,
        address = data['address'],
        city = data['city'],
        zipcode = data['zipcode'],
        phone = data['phone'],
        provincia = data['provincia'],
    )
    account.save()
    return account

def info_account(account, data):
    account.update(
        address = data['address'],
        city = data['city'],
        zipcode = data['zipcode'],
        phone = data['phone'],
        provincia = data['provincia'],
    )

@csrf_exempt
def create_user_data(data):

    user = User.objects.create_user(data['email'], data['email'], data['password'])
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.save()

    return user

@csrf_exempt
def create_user_(request):
    data = json.loads(request.body)
    print(data)
    data['user_bool'] = ''
    '''
    Si request.user.authenticated ->(1) Check if Acount, if not account -> Crear Acount -> Put all information in Account -> return
    No request.user.authenticated -> Check if in checkout form want an account('i_cuenta) -> Si -> Check if user exist -> Create User ->  (1)
                                                                                         -> No -> return
    '''
    user = request.user
    if(not user.is_authenticated):
        if(data['i_cuenta'] == 1):
            return JsonResponse({'data': data})
        else:
            if(User.objects.filter(email = data['email'] ).count() == 0):
                user = create_user_data(data)
            else:
                user = User.objects.get(email = data['email'])

                try:
                    if(data['is_register'] == True):
                        print('Usuario ya creado')
                        return JsonResponse({"data":{}})
                except: print('Error')

                if (not user.check_password(data['password'])):
                    print('None password')

                    print('Este email coincide con un usuario pero la contraseña no es correcta')
                    return JsonResponse({"data":{}})
    data['user_bool'] = user.email

    return JsonResponse({'data': data})

@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    print(data)
    if(User.objects.filter(email = data['email'] ).count() > 0):
        user = User.objects.get(email = data['email'])
        if (user.check_password(data['password'])):
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return JsonResponse({'data': data})
    else:
        return JsonResponse({"data":{}})

@csrf_exempt
def update_account(request):
    data = json.loads(request.body)
    user = User.objects.get(email = data['user_bool'])
    account = Account.objects.filter(user=user)

    if(not account):
        account = create_account(user, data)

    info_account(account, data)

    return JsonResponse({'data': data})

@csrf_exempt
def check_cart(request):
    cart = Cart(request)
    error = {}
    for item in cart:
        if(item['quantity'] > item['variant'].unidades):
            error[f"{item['variant'].id}"] = item['variant'].unidades
    
    print(len(error) > 0)
    if(len(error) > 0):
        return JsonResponse({'error': error})
    else:
        return JsonResponse({'error':{}})


@login_required
def my_account(request):
    return render(request, 'core/my_account.html')

@login_required
def my_orders(request):
    return render(request, 'core/my_orders.html')

@login_required
def my_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        user = request.user
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()

        account = Account.objects.filter(user=user)
        account.update(
            address = data['address'],
            city = data['city'],
            zipcode = data['zipcode'],
            phone = data['phone'],
            provincia = data['provincia'],
        )
        return JsonResponse({'data': data})

    return render(request, 'core/my_data.html')

@login_required
def my_favorites(request):

    lista = []
    if(request.user.is_authenticated):
        if(Account.objects.filter(user = request.user).exists()):
            if(Account.objects.filter(user = request.user).values('favorites')[0]['favorites']):
                for i in Account.objects.filter(user = request.user).values('favorites')[0]['favorites'].split(','):
                    id_col = i.replace('(', '').replace(')', '').split('/')
                    try:
                        lista.append(Variant.objects.filter(product = Product.objects.filter(id=int(id_col[0]))[0], color = Color.objects.filter(code = id_col[1])[0])[0].id)
                    except:
                        i = 0
        
    favorites = Variant.objects.filter(id__in = lista)

    context = {
        'favorites': favorites,
    }
    return render(request, 'core/my_favorites.html', context)

@login_required
def my_reviews(request):
    return render(request, 'core/my_reviews.html')

@login_required
def my_review(request, id):

    product = get_object_or_404(Product, id=id)
    
    if Review.objects.filter(product=product, created_by=request.user).exists():
        review = Review.objects.filter(product=product, created_by=request.user)[0]
    else: review = 0

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
                
            return JsonResponse({'data': data})

    
    context = {
        'review': review,
        'product': product,
    }
    return render(request, 'core/partials/my_review.html', context)



@login_required
def edit_my_account(request):

    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')
        user.save()
        return redirect('my_account')

    return render(request, 'core/edit_my_account.html')


def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    active_category = request.GET.get('category', '')

    if active_category:
        products = products.filter(categoria__slug=active_category)

    selecciones_query = []

    query = request.GET.get('query', '')


    if query:
        originals = products
        products = products.filter(sexo__contains=['1,0']);
        querys = query.split(':')
        for i in querys:
            products2 = originals.filter(Q(nombre__icontains=i) | Q(descripcion__icontains=i) | Q(categoria__slug__icontains=i))
            products = products | products2
        
        selecciones_query.append(query)

    #----------------------------------------------------------------

    '''PRECIO'''
    selecciones_price = []

    price = request.GET.get('price', '')

    if price:
        min_price = int(price.split(',')[0])
        max_price = int(price.split(',')[1])
        products = products.filter(precio__gte=min_price)
        products = products.filter(precio__lte=max_price)

        selecciones_price.append(f'{min_price},00€ - {max_price},00€')
    
    
    #----------------------------------------------------------------
    'SX'
    selecciones_sx = []

    sx = request.GET.get('sx','')
    
    if sx:
        sx = sx.split(':')
        if len(sx) < 4:
            original = products
            products = products.filter(sexo__contains=['1,0']);
            for i in sx:
                products2 = original.filter(Q(sexo__contains=i))
                products = products | products2

                selecciones_sx.append(i)
        
    #----------------------------------------------------------------
    '''TALLAS'''
    selecciones_sz = []

    sz = request.GET.get('sz','')
    
    if sz:
        sz = sz.split(':')
        original = products
        products = products.filter(sexo__contains=['1,0']);
        for i in original:
            for j in sz:
                list_v = Variant.objects.filter(product=i, size=str(j))
                if list_v.count() != 0:
                    products2 = original.filter(id=i.id)
                    products = products | products2
                    selecciones_sz.append(j)
                
    
    #----------------------------------------------------------------
    '''BRANDS'''
    if(len(products) == 0):
        if active_category:
            brands = Product.objects.filter(categoria__slug=active_category).values('marca')
        else:
            brands = Product.objects.all().values('marca')
    else: brands = products.values('marca')

    temp = []
    for i in brands:
        temp.append(i['marca'])
    temp = set(temp)
    brands = []
    for i in temp:
        brands.append(get_object_or_404(Marca,id=i))

    selecciones_ma = []

    ma = request.GET.get('ma','')
    
    if ma:
        ma = ma.split(':')
        original = products
        products = products.filter(sexo__contains=['1,0']);
        for j in ma:
            marca = get_object_or_404(Marca,slug=j)
            products2 = original.filter(marca=marca.id)
            products = products | products2

            selecciones_ma.append(j)
    #----------------------------------------------------------------
    '''ORDERING'''

    order = request.GET.get('or','')

    if (order == 'sort_popular'):
        products = products.order_by('-popular_rating')
    if (order == 'sort_price_asc'):
        products = products.order_by('precio')
    if (order == 'sort_price_desc'):
        products = products.order_by('-precio')

    #----------------------------------------------------------------
    'PRECIO MIN/MAX'
    min_max_price = products.aggregate(Min("precio"), Max("precio"))
        
    if(products):
        min_max_price['precio__min'] = math.floor(min_max_price['precio__min'])
        min_max_price['precio__max'] = math.ceil(min_max_price['precio__max'])

        if (products.count() == 1) & (min_max_price['precio__min'] == min_max_price['precio__max']):
            min_max_price['precio__max'] = min_max_price['precio__max'] + 1
    else:
        min_max_price['precio__min'] = 0
        min_max_price['precio__max'] = 100
    
    'SX'

    temp = list(products.values('sexo'))
    
    sexo_list = []
    for j in ['hombre', 'mujer', 'nino', 'nina']:
        for i in temp:
            length = len(str(i['sexo']).split(', '))

            for t in range(length):
                if str(i['sexo'][t]) == j and j not in sexo_list: sexo_list.append(j)

    '''TALLAS'''

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
    
    temp = []
    if products:
        for product in products:
            size = temp + unique(Variant.objects.filter(product=product).values('size'),'size')
            temp = size

    unique_size = []
    [unique_size.append(i) for i in temp if i not in unique_size]
    
    size_num = []
    size_let = []
    ordenar_num = []
    for i in unique_size:
        if i.replace(".", "").replace("(","").replace(")","").replace("/","").isdigit():
            size_num.append(i)
    
            num = i.replace(".", "/").replace("(","/").replace(")","").split("/")
            x1 = 0
            if(len(num) > 1):
                x1 = float(num[1]) / float(num[2])
            ordenar_num.append(float(num[0]) + x1)
        else: size_let.append(i)
    
    ordenado = sorted(ordenar_num, key = lambda x:float(x))

    temp = []
    for i in ordenado:
        for j in range(len(ordenar_num)):
            if i == ordenar_num[j]:
                temp.append(size_num[j])
    
    size_num = temp

    temp = []
    for j in ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', '3XL']:
        for i in size_let:
            if i == j and j not in temp: temp.append(j)
    size_let = temp



    variants = Variant.objects.filter(product__in=products)
    original = variants
    variants = variants.filter(size__contains=['_'])

    for i in products:
        variants_p = Variant.objects.filter(product=i)
        colors =  unique(list(variants_p.values('color')),'color')
        if(colors.count() > 1):
            t = 0
            for col in colors:
                if(t != 0):
                    first_variant = Variant.objects.filter(product=i, color=col)[0]
                    variants = variants | Variant.objects.filter(pk = first_variant.id)
                else: t = 1

    context = {
        'products': products,
        'variants': variants,
        'categories': categories,
        'active_category': active_category,
        'min_max_price': min_max_price,
        'size_num': size_num,
        'size_let': size_let,
        'brands': brands,
        'sexo_list': sexo_list,
        
        'selecciones_query': selecciones_query,
        'selecciones_price': selecciones_price,
        'selecciones_sx': selecciones_sx,
        'selecciones_sz': selecciones_sz,
        'selecciones_ma': selecciones_ma,

    }
    #update_favorito(request.user, 30)
    return render(request, 'core/shop.html', context)

def update_favorito(request, id, color, str):
    if(request.user.is_authenticated):
        account = Account.objects.filter(user=request.user)
        if(account):
            favorites = account.values("favorites")[0]['favorites']
            if(favorites != None):
                favorites = favorites.split(',')
            else:
                favorites = []
            if(str == 'quitar'):
                try:
                    favorites.remove(f'({id}/{color})')
                except:
                    print('Error removing')
            else:
                favorites.append(f'({id}/{color})')
                if(favorites[0]== '' ):
                    favorites.remove('')
            favorites = list(dict.fromkeys(favorites))
            favorites = ",".join(favorites)
            account.update(favorites = favorites)
        else:
            if (str == 'añadir'):
                Account.objects.create(user=request.user, favorites=f'({id}/{color})')
    
    return JsonResponse({'data': 1})

def tiendas(request):

    return render(request, 'core/partials/tiendas.html')

def contacto(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        name = data['name']
        email = data['email']
        content = data['content'] 

        from_email = settings.EMAIL_HOST_USER
        
        html = render_to_string('core/emails/contactform.html', {'name': name, 'email': email, 'content': content})

        send_mail(
            f'Consulta de {name}',
            content,
            email,
            [from_email],
            fail_silently=False,
            html_message=html,
        )
        return JsonResponse({'data': data})
    


    return render(request, 'core/partials/contacto.html')

def alquiler_material(request):

    alquiler = Alquiler.objects.first()

    return render(request, 'core/partials/alquiler_material.html', {'alquiler': alquiler})

def my_devoluciones(request, id, order_id):

    variant = Variant.objects.get(pk=id)
    order = Order.objects.get(pk=order_id)
    if request.user.is_authenticated:
        name_user = f'{request.user.first_name} {request.user.last_name}'
    else: name_user = ''
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('content')
        
        from_email = settings.EMAIL_HOST_USER
        
        variants_list = request.POST.get('variants')
        variants_list = variants_list.split(',')
        
        variants = Variant.objects.filter(id__in=variants_list)
        current_site = 'https://edscon.pythonanywhere.com'
        
        html = render_to_string('core/emails/devolucionesform.html', {'name': name, 'email': email, 'content': content, 'variants': variants, 'order': order, 'url': current_site})
        
        email_message = EmailMultiAlternatives(
            f'Consulta incidència o devolució de {name}',
            content,
            email,
            [from_email],
            reply_to=[email],  # Optional: Set the reply-to address
        )
        for key in request.FILES.keys():
            uploaded_file = request.FILES[key]
            email_message.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)

        email_message.attach_alternative(html, "text/html")
        
        email_message.send(fail_silently=False)

        return JsonResponse({'data': 1})

    return render(request, 'core/partials/my_devoluciones.html', {'variant': variant, 'order': order, 'name_user': name_user})

from datetime import datetime
def my_vista_producto(request, order_id):

    order = Order.objects.get(pk=order_id)

    time = date_by_adding_business_days(order.created_at, 1)
    print(order.created_at, time)
    return render(request, 'core/partials/my_vista_producto.html', {'order': order, 'time': time, 'now': datetime.now()})

@login_required
@csrf_exempt
def change_psw(request):
    data = json.loads(request.body)
    if(request.user.is_authenticated):
            user = request.user
            if (user.check_password(data['password_old'])):
                user.set_password(data['password_new'])
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return JsonResponse({'data': data})
    
    return JsonResponse({"data":{}})

def quienes_somos(request):

    return render(request, 'core/partials/footer/quienes-somos.html',)

def ventajas(request):

    return render(request, 'core/partials/footer/ventajas.html',)

def ayuda(request):

    return render(request, 'core/partials/footer/ayuda.html',)

def condiciones_legales(request):

    return render(request, 'core/partials/footer/condiciones_legales.html',)

def politica_de_privacidad(request):

    return render(request, 'core/partials/footer/politica_de_privacidad.html',)

def politica_de_cookies(request):

    return render(request, 'core/partials/footer/politica_de_cookies.html',)

def condiciones_generales_compra_web(request):

    return render(request, 'core/partials/footer/condiciones_generales_compra_web.html',)