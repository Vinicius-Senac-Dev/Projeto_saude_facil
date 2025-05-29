from django.shortcuts import render

def nova_consulta(request):
    return render(request, 'consultas/nova_consulta.html')

def consulta_pendente(request):
    return render(request, 'consultas/consulta_pendente.html')
