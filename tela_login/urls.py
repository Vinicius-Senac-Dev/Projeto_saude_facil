from django.urls import path
from . import views


urlpatterns = [
    path('', views.tela_login, name='tela_login')
]