from django.urls import path

from .views import start_order, create_payment

urlpatterns = [
    path('start_order/', start_order, name='start_order'),
    path('create_payment/', create_payment, name='create_payment'),

    
]