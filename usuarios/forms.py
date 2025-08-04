# Segundo passo, criar o arquivo forms.py e escrever esse código
#Criamos esse arquivo porque ao utilizar o django admin, ele utiliza o próprio formulário e como criamos a nossa própria classe, precisamos definir que ele utilize a nossa classe.

from django import forms
from django.contrib.auth import forms as auth_forms
from .models import Users, Especializacao, DadosMedico

# Agora, estamos herdando e sobreescrevendo a classe userChangeform e definimos a classe Users que também sobreescremos.
class UserChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = Users

#Preciso sobreescrever a classe que cria o usuário dentro do formulário
class UserCreationForm(auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = Users


class EspecializacaoForm(forms.ModelForm):
    """Formulário para criar/editar especializações"""
    class Meta:
        model = Especializacao
        fields = ['nome', 'descricao', 'codigo_cbo', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da especialização'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descrição da especialização'
            }),
            'codigo_cbo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código CBO (opcional)'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class DadosMedicoForm(forms.ModelForm):
    """Formulário para dados específicos do médico"""
    class Meta:
        model = DadosMedico
        fields = [
            'usuario', 'crm', 'uf_crm', 'especializacoes', 'valor_consulta', 
            'tempo_consulta', 'biografia', 'formacao', 'experiencia',
            'horario_inicio', 'horario_fim', 'dias_semana', 'ativo'
        ]
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'crm': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número do CRM'
            }),
            'uf_crm': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), 
                ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
                ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
                ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
                ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
                ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
                ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
                ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
                ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
                ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
            ]),
            'especializacoes': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
            'valor_consulta': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Valor da consulta'
            }),
            'tempo_consulta': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tempo em minutos'
            }),
            'biografia': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Biografia do médico'
            }),
            'formacao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Formação acadêmica'
            }),
            'experiencia': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Experiência profissional'
            }),
            'horario_inicio': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'horario_fim': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'dias_semana': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 1,2,3,4,5 (Segunda a Sexta)'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar apenas usuários com cargo de médico
        self.fields['usuario'].queryset = Users.objects.filter(cargo='M')
        
        # Adicionar classes CSS específicas
        for field_name, field in self.fields.items():
            if field_name not in ['especializacoes', 'ativo']:
                field.widget.attrs.update({'class': 'form-control'})


class CadastroMedicoForm(forms.ModelForm):
    """Formulário para cadastro completo de médico (usuário + dados)"""
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Users
        fields = ['username', 'email', 'first_name', 'last_name', 'cpf', 'telefone']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.cargo = 'M'  # Definir cargo como médico
        if commit:
            user.save()
        return user