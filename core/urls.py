from django.contrib.auth import views
from django.urls import path

from core.views import frontpage, shop, signup, myaccount, edit_myaccount
from product.views import product, marca, marcas, variant_product


urlpatterns = [
    path('', frontpage, name='frontpage'),
    path('signup/', signup, name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('myacount/', myaccount, name="myaccount"),
    path('myacount/edit/', edit_myaccount, name="edit_myaccount"),
    path('shop/', shop, name='shop'),
    path('shop/<slug:slug>', product, name='product'),
    path('shop/<slug:slug>/<slug:slug_color>', variant_product, name='variant_product'),
    path('shop/', marcas, name='shop'),
    path('marcas/<slug:slug>', marca, name='marca'),
]
