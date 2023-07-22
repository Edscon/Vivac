from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from product.models import Product, Category, Marca
from django.db.models import Min, Max

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

    query = request.GET.get('query', '')

    if query:
        products = products.filter(Q(nombre__icontains=query) | Q(
            descripcion__icontains=query) | Q(categoria__slug__icontains=query))

    min_max_price = products.aggregate(Min("precio"), Max("precio"))
        
    if(products):
        min_max_price['precio__min'] = math.floor(min_max_price['precio__min'])
        min_max_price['precio__max'] = math.ceil(min_max_price['precio__max'])

        if (products.count() == 1) & (min_max_price['precio__min'] == min_max_price['precio__max']):
            min_max_price['precio__max'] = min_max_price['precio__max'] + 1
    else:
        min_max_price['precio__min'] = 0
        min_max_price['precio__max'] = 100

    price = request.GET.get('price', '')

    if price:

        min_price = int(price.split(',')[0])
        max_price = int(price.split(',')[1])
        products = products.filter(precio__gte=min_price)
        products = products.filter(precio__lte=max_price)

    print(products)
    context = {
        'products': products,
        'categories': categories,
        'active_category': active_category,
        'min_max_price': min_max_price,
    }

    return render(request, 'core/shop.html', context)
