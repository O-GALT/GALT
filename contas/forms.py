from django import forms
from core.essenciais import TipoUsuario
from locais.models import Predio, Setor, PredioSetor, Sala
from ativos.models import Equipamento

class PredioForm(forms.ModelForm):
    class Meta:
        model = Predio
        fields = ['predio']
        labels = {
            'predio': 'Nome do Prédio',
        }
        widgets = {
            'predio': forms.TextInput(attrs={'class': '', 'placeholder': 'Prédio A'}),
        }

class SetorForm(forms.ModelForm):
    class Meta:
        model = Setor
        fields = ['setor']
        labels = {
            'setor': 'Nome do Setor',
        }
        widgets = {
            'setor': forms.TextInput(attrs={'class': '', 'placeholder': 'Setor A'}),
        }

#nao deveria existir esse form porque 'PredioSetor' é um campo do formulario de sala
class PredioSetorForm(forms.ModelForm):
    class Meta:
        model = PredioSetor
        fields = ['predio', 'setor']
        widgets = {
            'predio': forms.Select(attrs={'class': ''}),
            'setor': forms.Select(attrs={'class': ''}),
        }

class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['numero', 'estado_sala', 'localizacao', 'predio_setor']
        widgets = {
            'numero': forms.NumberInput(attrs={'class': '', 'placeholder': '101'}),
            'estado_sala': forms.Select(attrs={'class': ''}),
            'localizacao': forms.TextInput(attrs={'class': '', 'placeholder': 'Primeiro andar'}),
            'predio_setor': forms.Select(attrs={'class': '', 'placeholder': 'Selecione o prédio e setor'}),
        }

class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ['tipo', 'modelo', 'serial', 'posicao', 'estado_equipamento', 'sala']
        widgets = {
            'tipo': forms.Select(attrs={'class': ''}),
            'modelo': forms.TextInput(attrs={'class': '', 'placeholder': 'Modelo'}),
            'serial': forms.NumberInput(attrs={'class': '', 'placeholder': '123456'}),
            'posicao': forms.TextInput(attrs={'class': '', 'placeholder': 'Posição'}),
            'estado_equipamento': forms.Select(attrs={'class': ''}),
            'sala': forms.Select(attrs={'class': ''}),
        }
    
class UsuarioForm(forms.Form):
    username = forms.CharField(label='Nome de usuário', max_length=150, widget=forms.TextInput(attrs={'class': '', 'placeholder': 'username'}))
    email_pessoal = forms.EmailField(label='Email pessoal', widget=forms.EmailInput(attrs={'class': '', 'placeholder': 'email@dominio.com'}))
    email_escolar = forms.EmailField(label='Email escolar', widget=forms.EmailInput(attrs={'class': '', 'placeholder': 'email@dominio.com'}))
    senha = forms.CharField(label='Senha', max_length=20, widget=forms.PasswordInput(attrs={'class': '', 'placeholder': 'Senha'}))
    cpf = forms.CharField(label='CPF', max_length=13, widget=forms.TextInput(attrs={'class': '', 'placeholder': '000.000.000-00'}))
    telefone = forms.CharField(label='Telefone', max_length=13, widget=forms.TextInput(attrs={'class': '', 'placeholder': '(99) 12345-6789'}))
    tipo_usuario = forms.ChoiceField(label='Tipo de usuário', choices=TipoUsuario.choices, widget=forms.Select(attrs={'class': ''}))
