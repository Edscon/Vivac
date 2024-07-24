
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse

import logging
import requests
import time
from django.conf import settings

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

logger = logging.getLogger(__name__)

@user_passes_test(superuser_required, login_url='/admin/login/')
def complete_form(request):

    
    return JsonResponse({'status': 'failed', 'message': 'Método no permitido'}, status=405)
