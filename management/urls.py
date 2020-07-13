from django.urls import path
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('ip', csrf_exempt(views.DisplayIP.as_view()), name='display_ip'),
]