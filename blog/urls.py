from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('portfolio', views.project_list, name='project_list'),
    path('portfolio/<int:pk>', views.project_detail, name='project_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
