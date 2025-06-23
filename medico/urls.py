from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="tela_principal_medico"),
    path("nova_consulta_medico/", views.nova_consulta_medico, name="nova_consulta_medico"),
    path('consulta_pendente_medico/', views.consulta_pendente_medico, name='consulta_pendente_medico'),
    path('atestado_medico/', views.atestado_medico, name='atestado_medico'),
    path('prescricao_medico/', views.prescricao_medico, name='prescricao_medico'),
    path('emitir_prescricao_medico/', views.emitir_prescricao_medico, name='emitir_prescricao_medico'),
]