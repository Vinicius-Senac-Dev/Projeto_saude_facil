from django.shortcuts import render

def tela_principal(request):
    return render(request, 'tela_principal/tela_principal.html')
