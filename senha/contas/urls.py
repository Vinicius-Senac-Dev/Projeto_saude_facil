from django.urls import path
from . import views

urlpatterns = [
    path('redefinir-senha/', views.redefinir_senha, name='redefinir_senha'),
    path('redefinir-senha2/', views.redefinir_senha2, name='redefinir_senha2'),
]
