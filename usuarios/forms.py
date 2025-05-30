# Segundo passo, criar o arquivo forms.py e escrever esse código
#Criamos esse arquivo porque ao utilizar o django admin, ele utiliza o próprio formulário e como criamos a nossa própria classe, precisamos definir que ele utilize a nossa classe.

from django import forms
from django.contrib.auth import forms
from .models import Users

# Agora, estamos herdando e sobreescrevendo a classe userChangeform e definimos a classe Users que também sobreescremos.
class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = Users

#Preciso sobreescrever a classe que cria o usuário dentro do formulário
class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = Users