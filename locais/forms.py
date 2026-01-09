from django import forms

from locais.models import Predios, Setores, Salas
from contas.models import Usuarios
from ativos.models import Equipamentos

class PredioForm(forms.ModelForm):
    class Meta:
        model = Predios
        fields = ['predio']
        labels = {
            'predio': 'Nome do Prédio',
        }
        widgets = {
            'predio': forms.TextInput(attrs={'class': '', 'placeholder': 'Prédio A'}),
        }

class SetorForm(forms.ModelForm):
    class Meta:
        model = Setores
        fields = ['setor', 'localizacao', 'predio']
        labels = {
            'setor': 'Nome do Setor',
            'predio': 'predios',
            'localizacao': 'Localização do Setor',
        }
        widgets = {
            'setor': forms.TextInput(attrs={'class': '', 'placeholder': 'Setor A'}),
            'localizacao': forms.TextInput(attrs={'class': '', 'placeholder': 'Primeiro andar'}),
            'predio': forms.Select(attrs={'class': ''}),
        }

class SalaForm(forms.ModelForm):
    class Meta:
        model = Salas
        fields = ['estado_atual', 'localizacao', 'setor']
        widgets = {
            'estado_atual': forms.Select(attrs={'class': ''}),
            'localizacao': forms.TextInput(attrs={'class': '', 'placeholder': 'A17'}),
            'setor': forms.Select(attrs={'class': ''})
        }

class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamentos
        fields = ['sala', 'posicao', 'tipo', 'serial', 'estado_atual', 'fabricante', 'data_aquisicao']
        widgets = {
            'tipo': forms.Select(attrs={'class': ''}),
            'serial': forms.TextInput(attrs={'class': '', 'placeholder': 'SNX-8745-DF92'}),
            'posicao': forms.NumberInput(attrs={'class': '', 'placeholder': '0'}),
            'estado_atual': forms.Select(attrs={'class': ''}),
            'sala': forms.Select(attrs={'class': ''}),
            'fabricante': forms.TextInput(attrs={'class': '', 'placeholder': 'Fabricante'}),
            'data_aquisicao': forms.DateInput(attrs={'class': '', 'type': 'date'})
        }

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['email', 'email_escolar', 'cpf', 'numero', 'password', 'groups']
        labels = {
            'groups': 'Tipo de Usuario'
        }

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'exemplo@gmail.com'}),
            'email_escolar': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@escolar.com'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite a senha'}),
            'groups': forms.CheckboxSelectMultiple(attrs={'class': ''}),
        }