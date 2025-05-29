from django.urls import path
from . import views

urlpatterns = [
    path("nova_consulta/", views.nova_consulta, name="nova_consulta"),
    path('consulta_pendente/', views.consulta_pendente, name='consulta_pendente'),
]