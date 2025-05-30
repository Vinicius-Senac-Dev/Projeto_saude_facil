from django.urls import path
from .views import agendar_consulta

urlpatterns = [
    path('', agendar_consulta, name='agendar_consulta'),  # vazio, porque o prefixo já está no projeto
]
