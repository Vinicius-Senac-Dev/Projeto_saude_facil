from django.shortcuts import render
from django.http import HttpResponse
#Esse usuário tem superpoderes, porém é possível que outro usuário consiga acesso, para restringir isso, utilizamos o rolepermissions decorators.
from rolepermissions.decorators import has_permission_decorator
#E defino no has um cargo em especifico ou uma permissão para acessar essa página. 
#No caso estamos utilizando que apenas o usuario que tem a permissão cadastrar_recepcionista definido no role permissions, pode acessar a página cadastrar_recepcionista.
#Temos a opção has_role_decorator, onde podemos escolher o cargo ao inves da permissão.
@has_permission_decorator('cadastrar_recepcionista')
def cadastrar_recepcionista(request):
    return HttpResponse('Teste')