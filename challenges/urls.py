from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('challenge/<int:pk>/', views.challenge_detail, name='challenge_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


