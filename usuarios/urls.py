from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar_recepcionista/', views.cadastrar_recepcionista, name="cadastrar_recepcionista"),
    path('cadastro/', views.cadastro_publico, name='cadastro'),
    
    # URLs Administrativas
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Especializações
    path('especializacoes/', views.listar_especializacoes, name='listar_especializacoes'),
    path('especializacoes/criar/', views.criar_especializacao, name='criar_especializacao'),
    path('especializacoes/<int:pk>/editar/', views.editar_especializacao, name='editar_especializacao'),
    
    # Médicos
    path('medicos/', views.listar_medicos, name='listar_medicos'),
    path('medicos/criar/', views.criar_medico, name='criar_medico'),
    path('medicos/<int:pk>/dados/', views.editar_dados_medico, name='editar_dados_medico'),
    
    # Perfil do médico
    path('perfil-medico/', views.perfil_medico, name='perfil_medico'),
]
