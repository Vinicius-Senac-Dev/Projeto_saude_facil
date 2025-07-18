from django.contrib import admin
from django.urls import path

from historico import views

urlpatterns = [
    path('', views.historico, name='hitorico')
]