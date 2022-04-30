from django.contrib import admin
from django.urls import path, include
from .views import index, register

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name="register"),
]