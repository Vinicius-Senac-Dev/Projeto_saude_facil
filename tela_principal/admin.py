from django.contrib import admin
from .models import Consulta, HorarioAtendimento, IndisponibilidadeMedico


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'medico', 'especialidade', 'data_consulta', 'hora_consulta', 'status', 'tipo_convenio')
    list_filter = ('status', 'tipo_convenio', 'especialidade', 'data_consulta', 'criado_em')
    search_fields = ('paciente__username', 'paciente__first_name', 'paciente__last_name', 
                    'medico__username', 'medico__first_name', 'medico__last_name')
    readonly_fields = ('criado_em', 'atualizado_em')
    date_hierarchy = 'data_consulta'
    
    fieldsets = (
        ('Informações da Consulta', {
            'fields': ('paciente', 'medico', 'especialidade', 'data_consulta', 'hora_consulta')
        }),
        ('Detalhes', {
            'fields': ('motivo', 'observacoes', 'valor')
        }),
        ('Convênio', {
            'fields': ('tipo_convenio', 'plano_saude')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Auditoria', {
            'fields': ('criado_por', 'criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(HorarioAtendimento)
class HorarioAtendimentoAdmin(admin.ModelAdmin):
    list_display = ('medico', 'dia_semana', 'hora_inicio', 'hora_fim', 'ativo')
    list_filter = ('dia_semana', 'ativo')
    search_fields = ('medico__username', 'medico__first_name', 'medico__last_name')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Se for médico, mostrar apenas seus próprios horários
            if hasattr(request.user, 'cargo') and request.user.cargo == 'M':
                return qs.filter(medico=request.user)
        return qs


@admin.register(IndisponibilidadeMedico)
class IndisponibilidadeMedicoAdmin(admin.ModelAdmin):
    list_display = ('medico', 'data_inicio', 'data_fim', 'motivo', 'ativo')
    list_filter = ('ativo', 'data_inicio')
    search_fields = ('medico__username', 'medico__first_name', 'medico__last_name', 'motivo')
    date_hierarchy = 'data_inicio'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Se for médico, mostrar apenas suas próprias indisponibilidades
            if hasattr(request.user, 'cargo') and request.user.cargo == 'M':
                return qs.filter(medico=request.user)
        return qs
