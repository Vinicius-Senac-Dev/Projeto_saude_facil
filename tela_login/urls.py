from django.urls import path
from . import views


urlpatterns = [
    path('', views.tela_login, name='login'),
    path('medico/', views.login_medico, name='login_medico'),
    path('esqueci-senha/', views.esqueci_senha, name='esqueci_senha'),
    path('logout/', views.logout_view, name='logout')
]