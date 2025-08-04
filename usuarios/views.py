from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
#Esse usuário tem superpoderes, porém é possível que outro usuário consiga acesso, para restringir isso, utilizamos o rolepermissions decorators.
from rolepermissions.decorators import has_permission_decorator
#E defino no has um cargo em especifico ou uma permissão para acessar essa página. 
#No caso estamos utilizando que apenas o usuario que tem a permissão cadastrar_recepcionista definido no role permissions, pode acessar a página cadastrar_recepcionista.
#Temos a opção has_role_decorator, onde podemos escolher o cargo ao inves da permissão.
#Redirect redireciona para uma determinada página
from django.urls import reverse 
#Reverse serve para ao inves de passar o caminho da url, ele recebe o nome da url que quero e ele já recebe o caminho de forma automatica
from .models import Users, Especializacao, DadosMedico
#Importando a biblioteca Users para criar a verificação se o gerente está cadastrando uma mesma recepcionista, com o users não iremos permitir.

from django.contrib import auth
#Verificar se as credenciais existe no banco para realizar o login 

from .forms import EspecializacaoForm, DadosMedicoForm, CadastroMedicoForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from rolepermissions.checkers import has_permission
from django import forms 

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

def cadastro_publico(request):
    """View para cadastro público de usuários (pacientes)"""
    if request.method == 'GET':
        return render(request, 'usuarios/cadastro.html')
    
    elif request.method == 'POST':
        # Receber os dados do formulário
        username = request.POST.get('username')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        celular = request.POST.get('celular')
        termos = request.POST.get('termos')
        
        # Validações
        if not termos:
            messages.error(request, 'Você deve aceitar os termos e condições de uso.')
            return render(request, 'usuarios/cadastro.html')
        
        if senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'usuarios/cadastro.html')
        
        if len(senha) < 6:
            messages.error(request, 'A senha deve ter pelo menos 6 caracteres.')
            return render(request, 'usuarios/cadastro.html')
        
        # Verificar se usuário já existe
        if Users.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já existe.')
            return render(request, 'usuarios/cadastro.html')
        
        if Users.objects.filter(email=email).exists():
            messages.error(request, 'E-mail já cadastrado.')
            return render(request, 'usuarios/cadastro.html')
        
        # Verificar se CPF já existe (se fornecido)
        if cpf and Users.objects.filter(cpf=cpf).exists():
            messages.error(request, 'CPF já cadastrado.')
            return render(request, 'usuarios/cadastro.html')
        
        try:
            # Criar novo usuário como paciente
            user = Users.objects.create_user(
                username=username,
                email=email,
                password=senha,
                first_name=first_name,
                last_name=last_name,
                cargo='P',  # Paciente por padrão
                cpf=cpf if cpf else None,
                telefone=celular if celular else None
            )
            
            messages.success(request, f'Cadastro realizado com sucesso, {user.first_name or user.username}! Você pode fazer login agora.')
            return redirect('login')
            
        except Exception:
            messages.error(request, 'Erro ao criar conta. Tente novamente.')
            return render(request, 'usuarios/cadastro.html')


# ================= VIEWS ADMINISTRATIVAS =================

@login_required
@has_permission_decorator('gerenciar_dados')
def admin_dashboard(request):
    """Dashboard administrativo"""
    if not request.user.cargo == 'G':
        messages.error(request, 'Acesso negado. Apenas gerentes podem acessar esta área.')
        return redirect('tela_principal')
    
    # Estatísticas básicas
    total_medicos = Users.objects.filter(cargo='M').count()
    total_pacientes = Users.objects.filter(cargo='P').count()
    total_especializacoes = Especializacao.objects.filter(ativo=True).count()
    medicos_com_dados = DadosMedico.objects.filter(ativo=True).count()
    
    context = {
        'total_medicos': total_medicos,
        'total_pacientes': total_pacientes,
        'total_especializacoes': total_especializacoes,
        'medicos_com_dados': medicos_com_dados,
    }
    
    return render(request, 'usuarios/admin_dashboard.html', context)


@login_required
@has_permission_decorator('gerenciar_dados')
def listar_especializacoes(request):
    """Listar especializações médicas"""
    if not request.user.cargo == 'G':
        messages.error(request, 'Acesso negado.')
        return redirect('tela_principal')
    
    especializacoes = Especializacao.objects.all().order_by('nome')
    paginator = Paginator(especializacoes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'usuarios/especializacoes_list.html', {'page_obj': page_obj})


@login_required
@has_permission_decorator('gerenciar_dados')
def criar_especializacao(request):
    """Criar nova especialização"""
    if not request.user.cargo == 'G':
        messages.error(request, 'Acesso negado.')
        return redirect('tela_principal')
    
    if request.method == 'POST':
        form = EspecializacaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Especialização criada com sucesso!')
            return redirect('listar_especializacoes')
    else:
        form = EspecializacaoForm()
    
    return render(request, 'usuarios/especializacao_form.html', {'form': form, 'title': 'Criar Especialização'})


@login_required
@has_permission_decorator('gerenciar_dados')
def editar_especializacao(request, pk):
    """Editar especialização existente"""
    if not request.user.cargo == 'G':
        messages.error(request, 'Acesso negado.')
        return redirect('tela_principal')
    
    especializacao = get_object_or_404(Especializacao, pk=pk)
    
    if request.method == 'POST':
        form = EspecializacaoForm(request.POST, instance=especializacao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Especialização atualizada com sucesso!')
            return redirect('listar_especializacoes')
    else:
        form = EspecializacaoForm(instance=especializacao)
    
    return render(request, 'usuarios/especializacao_form.html', {
        'form': form, 
        'title': 'Editar Especialização',
        'especializacao': especializacao
    })


@login_required
@has_permission_decorator('gerenciar_dados')
def listar_medicos(request):
    """Listar médicos e seus dados"""
    if not request.user.cargo == 'G':
        messages.error(request, 'Acesso negado.')
        return redirect('tela_principal')
    
    medicos = Users.objects.filter(cargo='M').select_related().order_by('first_name', 'last_name')
    paginator = Paginator(medicos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'usuarios/medicos_list.html', {'page_obj': page_obj})


@login_required
@has_permission_decorator('gerenciar_dados')
def criar_medico(request):
    """Criar novo médico completo"""
    if not request.user.cargo == 'G':
        messages.error(request, 'Acesso negado.')
        return redirect('tela_principal')
    
    if request.method == 'POST':
        user_form = CadastroMedicoForm(request.POST)
        dados_form = DadosMedicoForm(request.POST)
        
        if user_form.is_valid() and dados_form.is_valid():
            # Salvar usuário
            user = user_form.save()
            
            # Salvar dados do médico
            dados_medico = dados_form.save(commit=False)
            dados_medico.usuario = user
            dados_medico.save()
            dados_form.save_m2m()  # Salvar relacionamentos many-to-many
            
            messages.success(request, f'Médico {user.get_full_name() or user.username} criado com sucesso!')
            return redirect('listar_medicos')
    else:
        user_form = CadastroMedicoForm()
        dados_form = DadosMedicoForm()
    
    return render(request, 'usuarios/medico_form.html', {
        'user_form': user_form,
        'dados_form': dados_form,
        'title': 'Cadastrar Médico'
    })


@login_required
@has_permission_decorator('gerenciar_dados')
def editar_dados_medico(request, pk):
    """Editar dados específicos do médico"""
    if not request.user.cargo == 'G':
        messages.error(request, 'Acesso negado.')
        return redirect('tela_principal')
    
    medico = get_object_or_404(Users, pk=pk, cargo='M')
    
    # Tentar obter dados médicos existentes ou criar novo
    try:
        dados_medico = medico.dadosmedico
    except DadosMedico.DoesNotExist:
        dados_medico = None
    
    if request.method == 'POST':
        form = DadosMedicoForm(request.POST, instance=dados_medico)
        if form.is_valid():
            dados = form.save(commit=False)
            dados.usuario = medico
            dados.save()
            form.save_m2m()
            messages.success(request, f'Dados do Dr(a). {medico.get_full_name() or medico.username} atualizados com sucesso!')
            return redirect('listar_medicos')
    else:
        form = DadosMedicoForm(instance=dados_medico)
        form.fields['usuario'].initial = medico
        form.fields['usuario'].widget.attrs['disabled'] = True
    
    return render(request, 'usuarios/dados_medico_form.html', {
        'form': form,
        'medico': medico,
        'title': f'Dados do Dr(a). {medico.get_full_name() or medico.username}'
    })


@login_required
def perfil_medico(request):
    """Perfil do médico logado"""
    if request.user.cargo != 'M':
        messages.error(request, 'Acesso negado. Apenas médicos podem acessar esta área.')
        return redirect('tela_principal')
    
    try:
        dados_medico = request.user.dadosmedico
    except DadosMedico.DoesNotExist:
        dados_medico = None
    
    if request.method == 'POST':
        form = DadosMedicoForm(request.POST, instance=dados_medico)
        if form.is_valid():
            dados = form.save(commit=False)
            dados.usuario = request.user
            dados.save()
            form.save_m2m()
            messages.success(request, 'Seus dados foram atualizados com sucesso!')
            return redirect('perfil_medico')
    else:
        form = DadosMedicoForm(instance=dados_medico)
        form.fields['usuario'].widget = forms.HiddenInput()
    
    return render(request, 'usuarios/perfil_medico.html', {
        'form': form,
        'dados_medico': dados_medico
    })