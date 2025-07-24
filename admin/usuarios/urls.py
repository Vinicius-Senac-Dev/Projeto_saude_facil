from django.urls import path
from . import views
urlpatterns = [
    path('cadastrar_recepcionista', views.cadastrar_recepcionista, name="cadastrar_recepcionista")
]
