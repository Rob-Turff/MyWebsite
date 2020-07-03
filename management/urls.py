from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('ip', views.display_ip, name='display_ip'),
]