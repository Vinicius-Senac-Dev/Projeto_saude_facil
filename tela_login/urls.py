from django.urls import path
from . import views


urlpatterns = [
    path('', views.tela_login, name='login'),
    path('esqueci-senha/', views.esqueci_senha, name='esqueci_senha'),
    path('logout/', views.logout_view, name='logout')
]