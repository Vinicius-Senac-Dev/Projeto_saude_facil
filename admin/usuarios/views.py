from django.shortcuts import render
from django.http import HttpResponse
#Esse usuário tem superpoderes, porém é possível que outro usuário consiga acesso, para restringir isso, utilizamos o rolepermissions decorators.
from rolepermissions.decorators import has_permission_decorator
#E defino no has um cargo em especifico ou uma permissão para acessar essa página. 
#No caso estamos utilizando que apenas o usuario que tem a permissão cadastrar_recepcionista definido no role permissions, pode acessar a página cadastrar_recepcionista.
#Temos a opção has_role_decorator, onde podemos escolher o cargo ao inves da permissão.
from django.shortcuts import redirect
#Redirect redireciona para uma determinada página
from django.urls import reverse 
#Reverse serve para ao inves de passar o caminho da url, ele recebe o nome da url que quero e ele já recebe o caminho de forma automatica
from .models import Users
#Importando a biblioteca Users para criar a verificação se o gerente está cadastrando uma mesma recepcionista, com o users não iremos permitir.

from django.contrib import auth
#Verificar se as credenciais existe no banco para realizar o login 

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
        user = Users.objects.create_user(username=email, email=email, password=senha, cargo='R')
        
        #TODO: Redirecionar com uma mensagem
        return HttpResponse('Conta criada')

def login(request):
    #Se for do tipo get
    if request.method == 'GET':
        #Se o usuario estiver autenticado, redireciona já para tela do sistema
        if request.user.is_authenticated:
            #reverse recebe a URL de forma automatica e o redirect já redireciona para o login
            return redirect(reverse('plataforma'))
        #Se o usuario não estiver autenticado redirecionar para tela de login
        return render(request, 'login.html')
    #Se o usuario estiver tentando fazer o login, recebe os dados do login
    elif request.method == 'POST':
        login = request.POST.get('email')
        senha = request.POST.get('senha')

    #Precisamos verificar se esse usuário existe no banco de dados, para isso precisamos importar a classe django.contrib auth que realiza essa validação.
    user = auth.authenticate(username=login, password=senha)

    if not user:
        #TODO: Redirecionar com mensagem de erro
        return HttpResponse('Usuário invalido')
    auth.login(request, user)
    return HttpResponse('Usuario logado com sucesso')
    
def logout(request):
    #Serve para limpar a nossa sessão.
    request.session.flush()
    return redirect(reverse('login'))