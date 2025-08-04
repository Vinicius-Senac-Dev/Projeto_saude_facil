from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
import logging

# Configurar o logger
logger = logging.getLogger(__name__)

# Usar o modelo de usuário configurado
User = get_user_model()

def tela_login(request):
    if request.method == 'POST':
        username_cpf = request.POST.get('username_cpf')
        password = request.POST.get('password')
        
        user = None
        
        # 1. Tentar autenticar diretamente com o valor fornecido como username
        user = authenticate(request, username=username_cpf, password=password)
        
        # 2. Se não funcionar e parece ser um email, tentar encontrar pelo email
        if not user and '@' in username_cpf:
            try:
                user_obj = User.objects.get(email=username_cpf)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        
        # 3. Se não funcionar e parece ser um CPF, tentar encontrar pelo CPF
        if not user and username_cpf.replace('.', '').replace('-', '').isdigit():
            try:
                # Remover formatação do CPF para busca
                cpf_limpo = username_cpf.replace('.', '').replace('-', '')
                user_obj = User.objects.get(cpf=cpf_limpo)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        
        if user is not None:
            login(request, user)
            nome_usuario = user.get_full_name() or user.first_name or user.username
            messages.success(request, f'Bem-vindo(a), {nome_usuario}!')
            return redirect('tela_principal')
        else:
            messages.error(request, 'Usuário ou senha inválidos. Por favor, tente novamente.')
    
    return render(request, 'login.html')

def esqueci_senha(request):
    if request.method == 'POST':
        username_cpf = request.POST.get('username_cpf')
        email = request.POST.get('email')
        
        user = None
        
        # Tentar encontrar o usuário de diferentes formas
        try:
            # Por username
            if not '@' in username_cpf:
                user = User.objects.get(username=username_cpf)
            # Por email
            else:
                user = User.objects.get(email=username_cpf)
        except User.DoesNotExist:
            # Por CPF se parecer um número
            if username_cpf.replace('.', '').replace('-', '').isdigit():
                try:
                    cpf_limpo = username_cpf.replace('.', '').replace('-', '')
                    user = User.objects.get(cpf=cpf_limpo)
                except User.DoesNotExist:
                    pass
        
        if user and user.email == email:
            # Gerar senha temporária
            temp_password = get_random_string(length=12)
            user.set_password(temp_password)
            user.save()
            
            # Tentar enviar e-mail
            try:
                nome_usuario = user.get_full_name() or user.first_name or user.username
                send_mail(
                    subject='Recuperação de Senha - Saúde Fácil',
                    message=f'''Olá {nome_usuario},

Você solicitou a recuperação de senha para sua conta no sistema Saúde Fácil.

Sua senha temporária é: {temp_password}

Por segurança:
1. Faça login com esta senha temporária
2. Altere sua senha assim que possível
3. Esta senha expira em 24 horas

Se você não solicitou esta recuperação, ignore este email.

Atenciosamente,
Equipe Saúde Fácil''',
                    from_email=None,  # Usa DEFAULT_FROM_EMAIL
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                messages.success(request, f'Uma nova senha foi enviada para {user.email}')
                return redirect('login')
            except Exception as e:
                logger.error(f"Erro ao enviar email: {e}")
                messages.error(request, 'Erro ao enviar email. Tente novamente mais tarde.')
        else:
            # Por segurança, não revelar se o usuário existe ou não
            messages.error(request, 'Dados informados não conferem. Verifique username/CPF e email.')
    
    return render(request, 'esqueci_senha.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Você saiu do sistema com sucesso!')
    return redirect('login')


def login_medico(request):
    """View específica para login de médicos"""
    if request.method == 'POST':
        username_cpf = request.POST.get('username_cpf')
        password = request.POST.get('password')
        
        user = None
        
        # 1. Verificar se é um CRM (pode ser usado como username ou cadastrado em dados médicos)
        if username_cpf.isdigit() or (username_cpf.isalnum() and len(username_cpf) >= 4):
            try:
                # Tentar buscar por CRM nos dados médicos
                from usuarios.models import DadosMedico
                dados_medico = DadosMedico.objects.get(crm=username_cpf)
                user = authenticate(request, username=dados_medico.usuario.username, password=password)
            except DadosMedico.DoesNotExist:
                # Se não encontrar por CRM, tentar como username normal
                user = authenticate(request, username=username_cpf, password=password)
        
        # 2. Se não funcionar e parece ser um email, tentar encontrar pelo email
        if not user and '@' in username_cpf:
            try:
                user_obj = User.objects.get(email=username_cpf)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        
        # 3. Se não funcionar e parece ser um CPF, tentar encontrar pelo CPF
        if not user and username_cpf.replace('.', '').replace('-', '').isdigit():
            try:
                # Remover formatação do CPF para busca
                cpf_limpo = username_cpf.replace('.', '').replace('-', '')
                user_obj = User.objects.get(cpf=cpf_limpo)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        
        # 4. Último recurso: tentar autenticação direta
        if not user:
            user = authenticate(request, username=username_cpf, password=password)
        
        if user is not None:
            # Verificar se o usuário é realmente um médico
            if hasattr(user, 'cargo') and user.cargo == 'M':
                login(request, user)
                nome_usuario = user.get_full_name() or user.first_name or user.username
                messages.success(request, f'Bem-vindo(a), Dr(a). {nome_usuario}!')
                
                # Redirecionar para área específica do médico
                return redirect('perfil_medico')
            else:
                messages.error(request, 'Este acesso é exclusivo para médicos. Use o login geral se você não é um médico.')
        else:
            messages.error(request, 'CRM, email/CPF ou senha inválidos. Verifique seus dados e tente novamente.')
    
    return render(request, 'login_medico.html')