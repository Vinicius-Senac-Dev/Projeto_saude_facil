from django.db import models
from django.contrib.auth import get_user_model
from usuarios.models import DadosMedico, Especializacao

User = get_user_model()


class Consulta(models.Model):
    TIPO_CONVENIO_CHOICES = [
        ('sus', 'SUS'),
        ('particular', 'Particular'),
        ('plano', 'Plano de Saúde'),
    ]
    
    STATUS_CHOICES = [
        ('agendada', 'Agendada'),
        ('confirmada', 'Confirmada'),
        ('realizada', 'Realizada'),
        ('cancelada', 'Cancelada'),
        ('faltou', 'Paciente Faltou'),
    ]
    
    PLANOS_SAUDE_CHOICES = [
        ('amil', 'Amil'),
        ('unimed', 'Unimed'),
        ('bradesco', 'Bradesco Saúde'),
        ('sulamerica', 'SulAmérica'),
        ('outros', 'Outros'),
    ]
    
    paciente = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'cargo': 'P'}, related_name='consultas_paciente')
    medico = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'cargo': 'M'}, related_name='consultas_medico')
    especialidade = models.ForeignKey(Especializacao, on_delete=models.CASCADE)
    
    data_consulta = models.DateField(verbose_name="Data da Consulta")
    hora_consulta = models.TimeField(verbose_name="Hora da Consulta")
    
    motivo = models.TextField(blank=True, null=True, verbose_name="Motivo da Consulta")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    tipo_convenio = models.CharField(max_length=20, choices=TIPO_CONVENIO_CHOICES, default='sus')
    plano_saude = models.CharField(max_length=20, choices=PLANOS_SAUDE_CHOICES, blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='agendada')
    
    valor = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="Valor da Consulta")
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultas_criadas')
    
    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
        ordering = ['data_consulta', 'hora_consulta']
        unique_together = ['medico', 'data_consulta', 'hora_consulta']
    
    def __str__(self):
        return f"{self.paciente.get_full_name() or self.paciente.username} - {self.data_consulta} {self.hora_consulta}"
    
    @property
    def nome_medico(self):
        return f"Dr(a). {self.medico.get_full_name() or self.medico.username}"
    
    @property
    def nome_paciente(self):
        return self.paciente.get_full_name() or self.paciente.username
    
    def get_status_display_class(self):
        """Retorna classe CSS baseada no status"""
        status_classes = {
            'agendada': 'warning',
            'confirmada': 'info',
            'realizada': 'success',
            'cancelada': 'danger',
            'faltou': 'secondary',
        }
        return status_classes.get(self.status, 'secondary')


class HorarioAtendimento(models.Model):
    """Modelo para definir horários de atendimento dos médicos"""
    DIAS_SEMANA_CHOICES = [
        (1, 'Segunda-feira'),
        (2, 'Terça-feira'),
        (3, 'Quarta-feira'),
        (4, 'Quinta-feira'),
        (5, 'Sexta-feira'),
        (6, 'Sábado'),
        (7, 'Domingo'),
    ]
    
    medico = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'cargo': 'M'})
    dia_semana = models.IntegerField(choices=DIAS_SEMANA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Horário de Atendimento"
        verbose_name_plural = "Horários de Atendimento"
        unique_together = ['medico', 'dia_semana', 'hora_inicio']
        ordering = ['dia_semana', 'hora_inicio']
    
    def __str__(self):
        return f"{self.medico.get_full_name() or self.medico.username} - {self.get_dia_semana_display()} {self.hora_inicio}-{self.hora_fim}"


class IndisponibilidadeMedico(models.Model):
    """Modelo para marcar dias/horários que o médico não está disponível"""
    medico = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'cargo': 'M'})
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    motivo = models.CharField(max_length=200, blank=True, null=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Indisponibilidade do Médico"
        verbose_name_plural = "Indisponibilidades dos Médicos"
        ordering = ['data_inicio']
    
    def __str__(self):
        return f"{self.medico.get_full_name() or self.medico.username} - {self.data_inicio.strftime('%d/%m/%Y %H:%M')} até {self.data_fim.strftime('%d/%m/%Y %H:%M')}"
