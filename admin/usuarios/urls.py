from django.urls import path
from . import views
urlpatterns = [
    path('cadastrar_recepcionista', views.cadastrar_recepcionista, name="cadastrar_recepcionista"),
    path('login/', views.login, name='login'),
    path('sair/', views.logout, name='sair')
]
