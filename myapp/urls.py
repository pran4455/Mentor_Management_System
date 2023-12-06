from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path("",views.home, name = "home"),
    path('login/', views.login, name='login'),
    path('addstudent/', views.addstudent, name='addstudent'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)