from django.shortcuts import render, redirect
from .models import Medico, Consulta
from django.utils import timezone

def agendar_consulta(request):
    medicos = Medico.objects.all()
    
    if request.method == 'POST':
        medico_id = request.POST['medico_id']
        data_hora = request.POST['data_hora']
        paciente_nome = request.POST['paciente_nome']
        Consulta.objects.create(
            medico_id=medico_id,
            data_hora=data_hora,
            paciente_nome=paciente_nome
        )
        return redirect('minhas_consultas')  # Suponha que essa rota exista

    return render(request, 'medico/agendar_consulta.html', {'medicos': medicos})
