from django.contrib.auth import views
from django.urls import path


from core.views import frontpage, shop, signup, my_account, my_orders, my_data, my_favorites, my_reviews, my_review, edit_my_account, create_user_, update_account, check_cart, quienes_somos, update_favorito, login_p, login_user, tiendas, contacto, alquiler_material, my_devoluciones, my_vista_producto
from product.views import product, marca, marcas, variant_product


urlpatterns = [
    path('', frontpage, name='frontpage'),
    path('signup/', signup, name='signup'),
    
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('login_p/', login_p, name="login_p"),
    path('login_user/', login_user, name="login_user"),

    path('my_account/', my_account, name="my_account"),
    path('my_account/orders/', my_orders, name="my_orders"),
    path('my_account/data/', my_data, name="my_data"),
    path('my_account/favorites/', my_favorites, name="my_favorites"),
    path('my_account/reviews/', my_reviews, name="my_reviews"),
    path('my_account/review/<int:id>', my_review, name="my_review"),
    path('my_account/edit/', edit_my_account, name="edit_my_account"),
    path('my_account/devoluciones/<int:id>/<int:order_id>', my_devoluciones, name="my_devoluciones"),
    path('my_account/my_vista_producto/<int:order_id>', my_vista_producto, name="my_vista_producto"),

    path('shop/', shop, name='shop'),
    path('shop/<slug:slug>', product, name='product'),
    path('shop/<slug:slug>/<slug:slug_color>', variant_product, name='variant_product'),
    path('marcas/<slug:slug>', marca, name='marca'),

    path('create_user_/', create_user_, name='create_user_'),
    path('update_account/', update_account, name='update_account'),
    path('check_cart/', check_cart, name='check_cart'),

    path('quienes-somos/', quienes_somos, name='quienes-somos'),
    path('alquiler_material/', alquiler_material, name='alquiler_material'),
    path('tiendas/', tiendas, name='tiendas'),
    path('contacto/', contacto, name='contacto'),

    path('update_favorito/<int:id>/<str:color>/<str:str>', update_favorito, name='update_favorito'),

]
