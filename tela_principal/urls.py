from django.urls import path
from . import views

urlpatterns = [
    path("", views.tela_principal, name="tela_principal"),
    
    # Agenda de Consultas
    path("agenda/", views.agenda_consultas, name="agenda_consultas"),
    path("agenda/nova/", views.nova_consulta, name="nova_consulta"),
    path("agenda/pendentes/", views.consultas_pendentes, name="consultas_pendentes"),
    
    # Prescrições e Atestados
    path("prescricoes/", views.prescricoes, name="prescricoes"),
    path("prescricoes/minhas/", views.minhas_prescricoes, name="minhas_prescricoes"),
    path("prescricoes/atestado/", views.emitir_atestado, name="emitir_atestado"),
    
    # Histórico de Consultas
    path("historico/", views.historico_consultas, name="historico_consultas"),
]