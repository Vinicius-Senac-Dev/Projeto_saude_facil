from django.db import models

class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome

class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data = models.DateField()
    hora = models.TimeField()
    observacoes = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pendente', 'Pendente'),
            ('realizada', 'Realizada'),
            ('cancelada', 'Cancelada')
        ],
        default='pendente'
    )

    def __str__(self):
        return f"Consulta de {self.paciente.nome} em {self.data.strftime('%d/%m/%Y')} às {self.hora.strftime('%H:%M')}"
