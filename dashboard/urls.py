from django.contrib.auth import views
from django.urls import path

from dashboard.views import dashboard, complete_form

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('complete_form', complete_form, name='complete_form'),
]