from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from usuarios.models import Especializacao, DadosMedico, Users
from .models import Consulta, HorarioAtendimento
import datetime
import json

@login_required(login_url='login')
def tela_principal(request):
    context = {
        'user_name': request.user.first_name if request.user.first_name else request.user.username,
        'page_title': 'Saúde Fácil - Página Principal'
    }
    return render(request, 'tela_principal/tela_principal.html', context)

# Agenda de Consultas
@login_required(login_url='login')
def agenda_consultas(request):
    context = {
        'page_title': 'Saúde Fácil - Agenda de Consultas',
        'current_date': timezone.now().strftime('%d/%m/%Y')
    }
    return render(request, 'tela_principal/agenda/agenda.html', context)

@login_required(login_url='login')
def nova_consulta(request):
    if request.method == 'POST':
        try:
            # Processar dados do formulário
            especialidade_id = request.POST.get('especialidade')
            medico_id = request.POST.get('medico')
            data_consulta = request.POST.get('data_consulta')
            hora_consulta = request.POST.get('hora_consulta')
            motivo = request.POST.get('motivo', '')
            tipo_convenio = request.POST.get('convenio', 'sus')
            plano_saude = request.POST.get('plano', '')
            
            # Validações
            if not all([especialidade_id, medico_id, data_consulta, hora_consulta]):
                messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
                return redirect('nova_consulta')
            
            # Buscar objetos
            especialidade = Especializacao.objects.get(id=especialidade_id)
            medico = Users.objects.get(id=medico_id, cargo='M')
            
            # Converter data e hora
            data_obj = datetime.datetime.strptime(data_consulta, '%Y-%m-%d').date()
            hora_obj = datetime.datetime.strptime(hora_consulta, '%H:%M').time()
            
            # Verificar se horário já está ocupado
            if Consulta.objects.filter(medico=medico, data_consulta=data_obj, hora_consulta=hora_obj).exists():
                messages.error(request, 'Este horário já está ocupado. Escolha outro horário.')
                return redirect('nova_consulta')
            
            # Criar consulta
            with transaction.atomic():
                Consulta.objects.create(
                    paciente=request.user,
                    medico=medico,
                    especialidade=especialidade,
                    data_consulta=data_obj,
                    hora_consulta=hora_obj,
                    motivo=motivo,
                    tipo_convenio=tipo_convenio,
                    plano_saude=plano_saude if tipo_convenio == 'plano' else None,
                    criado_por=request.user
                )
                
                messages.success(request, f'Consulta agendada com sucesso para {data_obj.strftime("%d/%m/%Y")} às {hora_obj.strftime("%H:%M")}!')
                return redirect('agenda_consultas')
                
        except Exception as e:
            messages.error(request, f'Erro ao agendar consulta: {str(e)}')
            return redirect('nova_consulta')
    
    # GET request - carregar dados para o formulário
    especialidades = Especializacao.objects.filter(ativo=True).order_by('nome')
    medicos_com_dados = Users.objects.filter(
        cargo='M',
        dadosmedico__ativo=True
    ).select_related('dadosmedico').order_by('first_name', 'last_name')
    
    hoje = timezone.now().date()
    max_date = hoje + datetime.timedelta(days=30)  # 30 dias à frente
    
    context = {
        'page_title': 'Saúde Fácil - Nova Consulta',
        'especialidades': especialidades,
        'medicos': medicos_com_dados,
        'today': hoje,
        'max_date': max_date,
    }
    return render(request, 'tela_principal/agenda/nova_consulta.html', context)


@login_required(login_url='login')
def buscar_medicos_por_especialidade(request):
    """AJAX: Buscar médicos por especialidade"""
    if request.method == 'GET':
        especialidade_id = request.GET.get('especialidade_id')
        
        if not especialidade_id:
            return JsonResponse({'medicos': []})
        
        try:
            # Buscar médicos que têm a especialidade selecionada
            medicos = Users.objects.filter(
                cargo='M',
                dadosmedico__ativo=True,
                dadosmedico__especializacoes__id=especialidade_id
            ).select_related('dadosmedico').distinct().order_by('first_name', 'last_name')
            
            medicos_data = []
            for medico in medicos:
                nome_completo = medico.get_full_name() or medico.username
                dados_medico = getattr(medico, 'dadosmedico', None)
                crm = f" - CRM: {dados_medico.crm}" if dados_medico and dados_medico.crm else ""
                
                medicos_data.append({
                    'id': medico.id,
                    'nome': f"Dr(a). {nome_completo}{crm}"
                })
            
            return JsonResponse({'medicos': medicos_data})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)


@login_required(login_url='login')
def buscar_horarios_disponiveis(request):
    """AJAX: Buscar horários disponíveis para um médico em uma data"""
    if request.method == 'GET':
        medico_id = request.GET.get('medico_id')
        data_str = request.GET.get('data')
        
        if not medico_id or not data_str:
            return JsonResponse({'horarios': []})
        
        try:
            # Converter string para data
            data_consulta = datetime.datetime.strptime(data_str, '%Y-%m-%d').date()
            dia_semana = data_consulta.isoweekday()  # 1=segunda, 7=domingo
            
            # Buscar médico
            medico = Users.objects.get(id=medico_id, cargo='M')
            dados_medico = getattr(medico, 'dadosmedico', None)
            
            if not dados_medico:
                return JsonResponse({'horarios': []})
            
            # Definir horários padrão baseados nos dados do médico
            horarios_base = []
            
            if dados_medico.horario_inicio and dados_medico.horario_fim:
                # Usar horários específicos do médico
                hora_atual = dados_medico.horario_inicio
                tempo_consulta = dados_medico.tempo_consulta or 30  # 30 min padrão
                
                while hora_atual < dados_medico.horario_fim:
                    horarios_base.append(hora_atual)
                    # Adicionar tempo da consulta
                    hora_atual = (datetime.datetime.combine(datetime.date.today(), hora_atual) + 
                                datetime.timedelta(minutes=tempo_consulta)).time()
            else:
                # Horários padrão: 8h às 17h, de 30 em 30 minutos
                for hora in range(8, 17):
                    horarios_base.append(datetime.time(hora, 0))
                    horarios_base.append(datetime.time(hora, 30))
            
            # Verificar dias de atendimento
            dias_atendimento = []
            if dados_medico.dias_semana:
                try:
                    dias_atendimento = [int(d.strip()) for d in dados_medico.dias_semana.split(',')]
                except (ValueError, AttributeError):
                    dias_atendimento = [1, 2, 3, 4, 5]  # Segunda a sexta padrão
            else:
                dias_atendimento = [1, 2, 3, 4, 5]  # Segunda a sexta padrão
            
            # Verificar se o médico atende no dia da semana selecionado
            if dia_semana not in dias_atendimento:
                return JsonResponse({'horarios': [], 'message': 'Médico não atende neste dia da semana'})
            
            # Buscar consultas já agendadas neste dia
            consultas_agendadas = Consulta.objects.filter(
                medico=medico,
                data_consulta=data_consulta,
                status__in=['agendada', 'confirmada']
            ).values_list('hora_consulta', flat=True)
            
            # Filtrar horários disponíveis
            horarios_disponiveis = []
            for horario in horarios_base:
                if horario not in consultas_agendadas:
                    horarios_disponiveis.append({
                        'hora': horario.strftime('%H:%M'),
                        'hora_formatada': horario.strftime('%H:%M')
                    })
            
            return JsonResponse({
                'horarios': horarios_disponiveis,
                'data_formatada': data_consulta.strftime('%d/%m/%Y')
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@login_required(login_url='login')
def consultas_pendentes(request):
    # Simulando algumas consultas pendentes
    consultas = [
        {'id': 1, 'data': '25/07/2025', 'hora': '14:30', 'especialidade': 'Cardiologia', 'medico': 'Dr. Carlos Silva'},
        {'id': 2, 'data': '30/07/2025', 'hora': '10:00', 'especialidade': 'Dermatologia', 'medico': 'Dra. Ana Pereira'},
        {'id': 3, 'data': '05/08/2025', 'hora': '09:15', 'especialidade': 'Clínica Geral', 'medico': 'Dr. Ricardo Santos'}
    ]
    
    context = {
        'page_title': 'Saúde Fácil - Consultas Pendentes',
        'consultas': consultas
    }
    return render(request, 'tela_principal/agenda/consultas_pendentes.html', context)

# Prescrições e Atestados
@login_required(login_url='login')
def prescricoes(request):
    context = {
        'page_title': 'Saúde Fácil - Prescrições e Atestados'
    }
    return render(request, 'tela_principal/prescricoes/prescricoes.html', context)

@login_required(login_url='login')
def minhas_prescricoes(request):
    # Simulando algumas prescrições
    prescricoes = [
        {'id': 1, 'data': '15/06/2025', 'medico': 'Dr. Carlos Silva', 'medicamentos': ['Paracetamol 750mg', 'Amoxicilina 500mg']},
        {'id': 2, 'data': '20/06/2025', 'medico': 'Dra. Ana Pereira', 'medicamentos': ['Dipirona 500mg', 'Hidrocortisona']},
        {'id': 3, 'data': '10/07/2025', 'medico': 'Dr. Ricardo Santos', 'medicamentos': ['Omeprazol 20mg', 'Ibuprofeno 600mg']}
    ]
    
    context = {
        'page_title': 'Saúde Fácil - Minhas Prescrições',
        'prescricoes': prescricoes
    }
    return render(request, 'tela_principal/prescricoes/minhas_prescricoes.html', context)

@login_required(login_url='login')
def emitir_atestado(request):
    context = {
        'page_title': 'Saúde Fácil - Emitir Atestado'
    }
    return render(request, 'tela_principal/prescricoes/emitir_atestado.html', context)

# Histórico de Consultas
@login_required(login_url='login')
def historico_consultas(request):
    # Para médicos, mostramos todas as últimas consultas realizadas por ele
    # Em um cenário real: consultas = Consulta.objects.filter(medico=request.user).order_by('-data')
    
    # Simulando consultas de um médico com dados de exemplo
    consultas = [
        {'id': 1, 'data': '15/07/2025', 'hora': '09:00', 'especialidade': 'Cardiologia', 'paciente': 'João Silva', 'idade': 45, 'diagnostico': 'Hipertensão arterial', 'status': 'Finalizada'},
        {'id': 2, 'data': '15/07/2025', 'hora': '10:30', 'especialidade': 'Cardiologia', 'paciente': 'Maria Oliveira', 'idade': 62, 'diagnostico': 'Arritmia cardíaca', 'status': 'Finalizada'},
        {'id': 3, 'data': '16/07/2025', 'hora': '14:00', 'especialidade': 'Cardiologia', 'paciente': 'Carlos Santos', 'idade': 53, 'diagnostico': 'Insuficiência cardíaca', 'status': 'Finalizada'},
        {'id': 4, 'data': '17/07/2025', 'hora': '11:15', 'especialidade': 'Cardiologia', 'paciente': 'Ana Ferreira', 'idade': 38, 'diagnostico': 'Avaliação de rotina', 'status': 'Finalizada'},
        {'id': 5, 'data': '18/07/2025', 'hora': '15:45', 'especialidade': 'Cardiologia', 'paciente': 'Paulo Costa', 'idade': 58, 'diagnostico': 'Infarto prévio - acompanhamento', 'status': 'Finalizada'},
        {'id': 6, 'data': '21/07/2025', 'hora': '08:00', 'especialidade': 'Cardiologia', 'paciente': 'Roberto Almeida', 'idade': 47, 'diagnostico': 'Em atendimento', 'status': 'Em andamento'},
    ]
    
    context = {
        'page_title': 'Saúde Fácil - Histórico de Consultas',
        'consultas': consultas
    }
    return render(request, 'historico/historico_consultas.html', context)
