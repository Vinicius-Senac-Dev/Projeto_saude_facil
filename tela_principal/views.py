from django.shortcuts import render

def home(request):
    return render(request, 'tela_principal/tela_principal.html')
