from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('accounts/', include('allauth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

'''urlpatterns += i18n_patterns(
    path('', include('core.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('accounts/', include('allauth.urls')),
    prefix_default_language=False,
)'''