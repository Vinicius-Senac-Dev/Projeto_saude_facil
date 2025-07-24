from django.shortcuts import render
from django.http import HttpResponse
#Esse usuário tem superpoderes, porém é possível que outro usuário consiga acesso, para restringir isso, utilizamos o rolepermissions decorators.
from rolepermissions.decorators import has_permission_decorator
#E defino no has um cargo em especifico ou uma permissão para acessar essa página. 
#No caso estamos utilizando que apenas o usuario que tem a permissão cadastrar_recepcionista definido no role permissions, pode acessar a página cadastrar_recepcionista.
#Temos a opção has_role_decorator, onde podemos escolher o cargo ao inves da permissão.

from .models import Users
#Importando a biblioteca Users para criar a verificação se o gerente está cadastrando uma mesma recepcionista, com o users não iremos permitir.
@has_permission_decorator('cadastrar_recepcionista')
def cadastrar_recepcionista(request):
    if request.method == "GET":
        return render(request, 'cadastrar_recepcionista.html')
    if request.method == "POST":
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        #Criando um filtro para saber o e-mail digitado gerente já existe dentro do nosso banco de dados
        user = Users.objects.filter(email=email)

        #Utilizando o método exists, que retorna true se existir um user na variável user e com isso apresenta httpResponse com a frase e-mail já existe
        if user.exists():
            #TODO: utilizar messages do django.
            return HttpResponse('E-mail já existe')
        
        #Cria um novo usuário/recepcionista se não existir
        #O django faz a autenticação usando o nome do usuário, por isso definimos que o username será o e-mail e definimos os outros campos que serão criados.
        user = Users.objects.create_user(username=email, email=email, password=senha)
        