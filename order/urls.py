from django.urls import path

from .views import create_payment

urlpatterns = [
    path('create_payment/', create_payment, name='create_payment'),
    
]