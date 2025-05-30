from django.db import models

class Medico(models.Model):
    nome = models.CharField(max_length=100)
    formacao = models.TextField()
    imagem = models.ImageField(upload_to='medicos/')

    def __str__(self):
        return self.nome

class Consulta(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    paciente_nome = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.paciente_nome} com {self.medico.nome} em {self.data_hora}"
