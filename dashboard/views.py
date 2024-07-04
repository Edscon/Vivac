from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

from order.models import Order

# Define si el usuario es un superuser
def superuser_required(user):
    return user.is_superuser

@user_passes_test(superuser_required, login_url='/admin/login/')
def dashboard(request):

    orders = Order.objects.all()

    context = {
        'orders': orders,
    }

    return render(request, 'dashboard/dashboard.html', context)
