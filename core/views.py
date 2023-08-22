from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Case, When
from product.models import Product, Category, Marca, Variant, Color
from django.db.models import Min, Max
from functools import reduce

import pandas as pd
import operator
import math

from .forms import SignUpForm



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

    context = {
        'products': products,
        'categories': categories,
        'marcas': marcas,
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


@login_required
def myaccount(request):
    return render(request, 'core/myaccount.html')


@login_required
def edit_myaccount(request):

    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')
        user.save()
        return redirect('myaccount')

    return render(request, 'core/edit_myaccount.html')


def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    active_category = request.GET.get('category', '')

    if active_category:
        products = products.filter(categoria__slug=active_category)

    selecciones_querry = []

    query = request.GET.get('query', '')


    if query:
        originals = products
        products = products.filter(sexo__contains=['1,0']);
        querys = query.split(':')
        for i in querys:
            products2 = originals.filter(Q(nombre__icontains=i) | Q(descripcion__icontains=i) | Q(categoria__slug__icontains=i))
            products = products | products2
        
        selecciones_querry.append(query)

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
    print(order)

    if (order == 'sort_popular'):
        products = products.order_by('-popular_rating')
    if (order == 'sort_price_asc'):
        products = products.order_by('precio')
    if (order == 'sort_price_desc'):
        products = products.order_by('-precio')

    #----------------------------------------------------------------
    print(products)

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
    print(temp)
    sexo_list = []
    for j in ['hombre', 'mujer', 'nino', 'nina']:
        for i in temp:
            leng = len(str(i['sexo']).split(', '))

            for t in range(leng):
                if str(i['sexo'][t]) == j and j not in sexo_list: sexo_list.append(j)
            
    
    print(sexo_list)

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



    '''BRANDS'''

    brands = products.values('marca')
    temp = []
    for i in brands:
        temp.append(i['marca'])
    temp = set(temp)
    brands = []
    for i in temp:
        brands.append(get_object_or_404(Marca,id=i))


    context = {
        'products': products,
        'categories': categories,
        'active_category': active_category,
        'min_max_price': min_max_price,
        'size_num': size_num,
        'size_let': size_let,
        'brands': brands,
        'sexo_list': sexo_list,
        
        'selecciones_querry': selecciones_querry,
        'selecciones_price': selecciones_price,
        'selecciones_sx': selecciones_sx,
        'selecciones_sz': selecciones_sz,
        'selecciones_ma': selecciones_ma,

    }

    return render(request, 'core/shop.html', context)
