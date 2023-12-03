from django.contrib.auth import views
from django.urls import path


from core.views import frontpage, shop, signup, myaccount, edit_myaccount, create_user_, update_account, quienes_somos, update_favorito, login_p
from product.views import product, marca, marcas, variant_product


urlpatterns = [
    path('', frontpage, name='frontpage'),
    path('signup/', signup, name='signup'),
    
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('login_p/', login_p, name="login_p"),

    path('myacount/', myaccount, name="myaccount"),
    path('myacount/edit/', edit_myaccount, name="edit_myaccount"),
    path('shop/', shop, name='shop'),
    path('shop/<slug:slug>', product, name='product'),
    path('shop/<slug:slug>/<slug:slug_color>', variant_product, name='variant_product'),
    path('marcas/<slug:slug>', marca, name='marca'),

    path('create_user_/', create_user_, name='create_user_'),
    path('update_account/', update_account, name='update_account'),

    path('quienes-somos/', quienes_somos, name='quienes-somos'),
    path('update_favorito/<int:id>/<str:color>/<str:str>', update_favorito, name='update_favorito'),

]
