from django.shortcuts import render, redirect
from django.contrib import messages

def redefinir_senha(request):
    return render(request, 'contas/redefinir_senha.html')

def redefinir_senha2(request):
    return render(request, 'contas/redefinir_senha2.html')