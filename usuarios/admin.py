# Terceiro passo, preciso registrar o usuário que criei no admin do django para poder aparecer
from django.contrib import admin
from .models import Users, Especializacao, DadosMedico
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
        ('Dados Pessoais', {'fields': ('cargo', 'cpf', 'telefone')}),
    )
    
    # Campos para adicionar novo usuário
    add_fieldsets = admin_auth_django.UserAdmin.add_fieldsets + (
        ('Dados Pessoais', {'fields': ('cargo', 'cpf', 'telefone', 'email', 'first_name', 'last_name')}),
    )
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'cargo', 'is_staff', 'is_active')
    list_filter = ('cargo', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'cpf')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Se não for superuser, mostrar apenas usuários que podem gerenciar
            if hasattr(request.user, 'cargo') and request.user.cargo == 'G':
                return qs
            return qs.filter(pk=request.user.pk)
        return qs


@admin.register(Especializacao)
class EspecializacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo_cbo', 'ativo', 'criado_em')
    list_filter = ('ativo', 'criado_em')
    search_fields = ('nome', 'codigo_cbo', 'descricao')
    list_editable = ('ativo',)
    readonly_fields = ('criado_em', 'atualizado_em')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'codigo_cbo', 'ativo')
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DadosMedico)
class DadosMedicoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'crm', 'uf_crm', 'get_especializacoes', 'valor_consulta', 'ativo')
    list_filter = ('uf_crm', 'ativo', 'especializacoes', 'criado_em')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name', 'crm')
    list_editable = ('ativo',)
    readonly_fields = ('criado_em', 'atualizado_em')
    filter_horizontal = ('especializacoes',)
    
    fieldsets = (
        ('Dados Básicos', {
            'fields': ('usuario', 'crm', 'uf_crm', 'especializacoes')
        }),
        ('Informações Profissionais', {
            'fields': ('biografia', 'formacao', 'experiencia'),
            'classes': ('collapse',)
        }),
        ('Configurações de Consulta', {
            'fields': ('valor_consulta', 'tempo_consulta', 'horario_inicio', 'horario_fim', 'dias_semana')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Se for médico, mostrar apenas seus próprios dados
            if hasattr(request.user, 'cargo') and request.user.cargo == 'M':
                return qs.filter(usuario=request.user)
            # Se for gerente, mostrar todos
            elif hasattr(request.user, 'cargo') and request.user.cargo == 'G':
                return qs
            # Outros cargos não veem dados médicos
            return qs.none()
        return qs
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "usuario":
            kwargs["queryset"] = Users.objects.filter(cargo='M')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)