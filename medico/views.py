from django.shortcuts import render

def home(request):
    return render(request, 'medico/tela_principal.html')

def nova_consulta(request):
    return render(request, 'medico/nova_consulta.html')

def consulta_pendente(request):
    return render(request, 'medico/consulta_pendente.html',)
    