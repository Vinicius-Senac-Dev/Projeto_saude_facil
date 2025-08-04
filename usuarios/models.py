from django.db import models
# Herdando a classe
from django.contrib.auth.models import AbstractUser
# Primeiro passo
# O django tem uma classe de autenticação já com alguns atributos, queremos inserir mais campos de atributos para definir os nossos próprios atributos, por isso, iremos herdar a classe User para sobreescrever os atributos.

# Acessando a classe e definindo o nosso atributo.
# Criando um novo campo com os nossos atributos, sobreescrevendo
class Users(AbstractUser):
    # Definindo os cargos de acesso ao sistema
    choices_cargo = (('R', 'Recepcionista'),
                     ('M', 'Médico'),
                     ('G', 'Gerente'),
                     ('P', 'Paciente'))
    cargo = models.CharField(max_length=1, choices=choices_cargo, default='P')
    cpf = models.CharField(max_length=14, blank=True, null=True, unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.username


class Especializacao(models.Model):
    """Modelo para especialidades médicas"""
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da Especialização")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    codigo_cbo = models.CharField(max_length=10, blank=True, null=True, verbose_name="Código CBO")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Especialização"
        verbose_name_plural = "Especializações"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class DadosMedico(models.Model):
    """Modelo para dados específicos dos médicos"""
    usuario = models.OneToOneField(Users, on_delete=models.CASCADE, limit_choices_to={'cargo': 'M'})
    crm = models.CharField(max_length=15, unique=True, verbose_name="CRM")
    uf_crm = models.CharField(max_length=2, verbose_name="UF do CRM")
    especializacoes = models.ManyToManyField(Especializacao, verbose_name="Especializações")
    valor_consulta = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="Valor da Consulta")
    tempo_consulta = models.PositiveIntegerField(default=30, verbose_name="Tempo de Consulta (minutos)")
    biografia = models.TextField(blank=True, null=True, verbose_name="Biografia")
    formacao = models.TextField(blank=True, null=True, verbose_name="Formação Acadêmica")
    experiencia = models.TextField(blank=True, null=True, verbose_name="Experiência Profissional")
    horario_inicio = models.TimeField(blank=True, null=True, verbose_name="Horário de Início")
    horario_fim = models.TimeField(blank=True, null=True, verbose_name="Horário de Fim")
    dias_semana = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Dias da Semana",
        help_text="Ex: 1,2,3,4,5 (Segunda a Sexta)"
    )
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Dados do Médico"
        verbose_name_plural = "Dados dos Médicos"
    
    def __str__(self):
        return f"Dr(a). {self.usuario.get_full_name() or self.usuario.username} - CRM: {self.crm}"
    
    def get_especializacoes(self):
        return ", ".join([esp.nome for esp in self.especializacoes.all()])
    
    def get_dias_semana_display(self):
        if not self.dias_semana:
            return ""
        dias = {
            '1': 'Segunda',
            '2': 'Terça', 
            '3': 'Quarta',
            '4': 'Quinta',
            '5': 'Sexta',
            '6': 'Sábado',
            '7': 'Domingo'
        }
        return ", ".join([dias.get(d, d) for d in self.dias_semana.split(',')])