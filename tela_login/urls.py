
from django.contrib import admin
from django.urls import path

from tela_login import views

urlpatterns = [
    path('', views.tela_login, name= 'tela_login')
]
