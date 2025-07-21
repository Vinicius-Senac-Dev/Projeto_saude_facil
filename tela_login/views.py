from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
import logging

# Configurar o logger
logger = logging.getLogger(__name__)

def tela_login(request):
    if request.method == 'POST':
        username_cpf = request.POST.get('username_cpf')
        password = request.POST.get('password')
        
        # Tentar autenticar com o nome de usuário fornecido
        user = authenticate(request, username=username_cpf, password=password)
        
        # Se não funcionar e o input parece ser um CPF, tentar encontrar o usuário pelo CPF
        if not user and username_cpf.isdigit():
            try:
                # Aqui assumimos que o CPF está armazenado no campo 'username'
                # Você pode adaptar isso se o CPF estiver em outro campo
                user_obj = User.objects.get(username=username_cpf)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        
        # Se não funcionar e o input parece ser um e-mail, tentar encontrar o usuário pelo e-mail
        if not user and '@' in username_cpf:
            try:
                user_obj = User.objects.get(email=username_cpf)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo(a), {user.first_name if user.first_name else user.username}!')
            # Redirecionar para a página principal após o login
            return redirect('tela_principal')  # Ajuste conforme o nome da sua URL para a tela principal
        else:
            messages.error(request, 'Usuário ou senha inválidos. Por favor, tente novamente.')
    
    return render(request, 'login.html')

def esqueci_senha(request):
    if request.method == 'POST':
        username_cpf = request.POST.get('username_cpf')
        email = request.POST.get('email')
        
        # Verificar se o usuário existe
        try:
            user = User.objects.get(username=username_cpf) if '@' not in username_cpf else User.objects.get(email=username_cpf)
            
            # Verificar se o e-mail informado corresponde ao do usuário
            if user.email == email:
                # Gerar senha temporária
                temp_password = get_random_string(length=12)
                user.set_password(temp_password)
                user.save()
                
                # Enviar e-mail com a senha temporária
                try:
                    send_mail(
                        'Recuperação de Senha - Saúde Fácil',
                        f'Olá {user.first_name},\n\nVocê solicitou a recuperação de senha.\n\nSua senha temporária é: {temp_password}\n\nPor favor, faça login e altere sua senha assim que possível.\n\nAtenciosamente,\nEquipe Saúde Fácil',
                        'seuapp@gmail.com',  # Substitua pelo seu e-mail
                        [user.email],
                        fail_silently=False,
                    )
                    messages.success(request, 'Uma nova senha foi enviada para o seu e-mail.')
                    return redirect('login')
                except Exception as e:
                    logger.error(f"Erro ao enviar email: {e}")
                    messages.error(request, 'Ocorreu um erro ao enviar o e-mail. Por favor, tente novamente mais tarde.')
            else:
                messages.error(request, 'O e-mail informado não corresponde ao usuário.')
        except User.DoesNotExist:
            # Não informamos que o usuário não existe por razões de segurança
            messages.error(request, 'Se o usuário existir, enviaremos um e-mail com instruções para recuperação de senha.')
        except Exception as e:
            logger.error(f"Erro na recuperação de senha: {e}")
            messages.error(request, 'Ocorreu um erro. Por favor, tente novamente mais tarde.')
    
    return render(request, 'esqueci_senha.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Você saiu do sistema com sucesso!')
    return redirect('login')