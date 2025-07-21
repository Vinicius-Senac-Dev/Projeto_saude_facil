# Terceiro passo, preciso registrar o usuário que criei no admin do django para poder aparecer
from django.contrib import admin
from .models import Users
# O as é para definir como quero chamar o aquela importação.
from django.contrib.auth import admin as admin_auth_django
from .forms import UserChangeForm, UserCreationForm

#Registrando o usuário que criamos na tela do django
@admin.register(Users)

#Como quero manter a página de admin do django e quero apenas inserir os campos cargos, preciso herdar de admin_auth_django e como quero pegar a classe do django preciso do acessar a classe UserAdmin, essa classe é a responsagel por toda página de admin, como layout, aparência, designer e configuração.
#Agora estamos inserindo os nossos atributos dentro da classe UserAdmin
class UsersAdmin(admin_auth_django.UserAdmin):
    #Ao invés do django utilizar as configurações com os seus campos padrões, ele vai utilizar os campos que criei, se a gente acessar a classe UserAdmin vamos ver as seguintes variáveis form, add_form e model, vamos sobreescrever essas variáveis passando os nossos atributos e classes que criamos.
    form = UserChangeForm
    add_form = UserCreationForm
    model = Users
    #Na classe forme eu já tenho campos criados e não quero perder esses campos que são personal info, permissions..., então eu acesso a variável fieldsets e passo para ele o meu usuário criado inserindo o meu fildset dentro da classe UserAdmin e para isso preciso passar como tupla definindo o nome do meu fildset.
    fieldsets = admin_auth_django.UserAdmin.fieldsets + (
        ('Cargo', {'fields': ('cargo',)}),
    )