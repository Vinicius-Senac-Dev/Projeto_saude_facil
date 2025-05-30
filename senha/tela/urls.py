from django.contrib import admin
from django.urls import path
from medico.views import agendar_consulta

urlpatterns = [
    path('', agendar_consulta, name='home'),  # raiz agora abre agendar_consulta
    path('admin/', admin.site.urls),
]
