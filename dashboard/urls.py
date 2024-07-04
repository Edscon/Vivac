from django.contrib.auth import views
from django.urls import path

from dashboard.views import dashboard

urlpatterns = [
    path('', dashboard, name='dashboard'),
]