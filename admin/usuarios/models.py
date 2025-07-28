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
                     ('G', 'Gerente'))
    cargo = models.CharField(max_length=1, choices=choices_cargo)