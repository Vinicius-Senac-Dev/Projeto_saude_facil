from django.shortcuts import render

def home(request):
    return render(request, 'paciente/tela_principal.html')

def nova_consulta(request):
    return render(request, 'paciente/nova_consulta.html')

def consulta_pendente(request):
    return render(request, 'paciente/consulta_pendente.html')