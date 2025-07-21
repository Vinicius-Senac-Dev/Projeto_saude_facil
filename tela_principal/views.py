from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime

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
    # Simulando disponibilidade de horários para os próximos 7 dias
    hoje = timezone.now().date()
    horarios_disponiveis = []
    
    for i in range(7):  # próximos 7 dias
        data = hoje + datetime.timedelta(days=i)
        # Horários disponíveis das 8h às 17h, de hora em hora
        for hora in range(8, 18):
            horarios_disponiveis.append({
                'data': data.strftime('%d/%m/%Y'),
                'dia_semana': ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'][data.weekday()],
                'hora': f'{hora:02d}:00'
            })
    
    context = {
        'page_title': 'Saúde Fácil - Nova Consulta',
        'horarios_disponiveis': horarios_disponiveis,
        'especialidades': ['Clínica Geral', 'Cardiologia', 'Dermatologia', 'Pediatria', 'Ortopedia']
    }
    return render(request, 'tela_principal/agenda/nova_consulta.html', context)

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
