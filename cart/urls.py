from django.urls import path

from cart.views import add_to_cart, cart, checkout, change_cart, hx_menu_cart, update_cart, hx_cart_total, hx_minicart, hx_addtocart, hx_minicart_icon_num
from order.views import payment_canceled, success, stripe_webhook


urlpatterns = [
    path('', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('change_cart/', change_cart, name='change_cart'),

    path('add_to_cart/<int:product_id>/<str:color>/<str:size>', add_to_cart, name='add_to_cart'),
    path('update_cart/<int:product_id>/<str:color>/<str:size>/<str:action>/', update_cart, name="update_cart"),

    path('hx_menu_cart/', hx_menu_cart, name="hx_menu_cart"),
    path('hx_cart_total/', hx_cart_total, name="hx_cart_total"),
    path('hx_minicart/', hx_minicart, name="hx_minicart"),
    path('hx_addtocart/', hx_addtocart, name="hx_addtocart"),
    path('hx_minicart_icon_num/', hx_minicart_icon_num, name="hx_minicart_icon_num"),


    path('success/', success, name='success'),
    path('payment_canceled/', payment_canceled, name='payment_canceled'),
    path('stripe_webhook/', stripe_webhook, name='stripe_webhook'),
]