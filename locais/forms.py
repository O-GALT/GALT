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
            'predio': forms.TextInput(attrs={
                'required': 'required',
                'oninvalid': "this.setCustomValidity('Nome do prédio é obrigatório.')",
                'oninput': "this.setCustomValidity('')",
                'placeholder': 'Prédio A',
                'maxlength': '30',
            }),
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
            'setor': forms.TextInput(attrs={
                'required': 'required',
                'oninvalid': "this.setCustomValidity('Nome do setor é obrigatório.')",
                'oninput': "this.setCustomValidity('')",
                'placeholder': 'Setor A',
                'maxlength': '30',
            }),
            'localizacao': forms.TextInput(attrs={
                'placeholder': 'Primeiro andar',
                'oninvalid': "this.setCustomValidity('Localização do setor é obrigatória.')",
                'oninput': "this.setCustomValidity('')",
                'placeholder': 'Primeiro andar',
                'maxlength': '50',
            }),
            'predio': forms.Select(attrs={
                'oninvalid': "this.setCustomValidity('Prédio a qual pertence é obrigatório.')",
                'oninput': "this.setCustomValidity('')",
            }),
        }

class SalaForm(forms.ModelForm):
    class Meta:
        model = Salas
        fields = ['estado_atual', 'localizacao', 'setor']
        widgets = {
            'estado_atual': forms.Select(attrs={
                'oninvalid': "this.setCustomValidity('Estado atual é obrigatório.')",
                'oninput': "this.setCustomValidity('')",
            }),
            'localizacao': forms.TextInput(attrs={
                'placeholder': 'A17',
                'oninvalid': "this.setCustomValidity('Localização é obrigatória.')",
                'oninput': "this.setCustomValidity('')",
                'maxlength': '50',
            }),
            'setor': forms.Select(attrs={
                'oninvalid': "this.setCustomValidity('Setor a qual pertence é obrigatório.')",
                'oninput': "this.setCustomValidity('')",
            })
        }

class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamentos
        fields = ['sala', 'posicao', 'tipo', 'serial', 'estado_atual', 'fabricante', 'data_aquisicao', 'fileira']
        widgets = {
            'tipo': forms.Select(attrs={
                'oninvalid': "this.setCustomValidity('Tipo de equipamento é obrigatório.')",
                'oninput': "this.setCustomValidity('')",
            }),
            'serial': forms.TextInput(attrs={
                'placeholder': 'SNX-8745-DF92',
                'oninvalid': "this.setCustomValidity('Serial do equipamento é obrigatório.')",
                'oninput': "this.setCustomValidity('')",
                'maxlength': '50',
            }),
            'posicao': forms.NumberInput(attrs={
                'placeholder': '0',
                'oninvalid': "this.setCustomValidity('Posição do equipamento é obrigatória.')",
                'oninput': "this.setCustomValidity('')",
                'min': '0',
                'step': '1',
            }),
            'estado_atual': forms.Select(attrs={
                'oninvalid': "this.setCustomValidity('Estado atual do equipamento é obrigatório.')",
                'oninput': "this.setCustomValidity('')",
            }),
            'sala': forms.Select(attrs={
                'oninvalid': "this.setCustomValidity('Sala onde o equipamento está localizado é obrigatória.')",
                'oninput': "this.setCustomValidity('')",
            }),
            'fileira': forms.Select(attrs={
                'oninvalid': "this.setCustomValidity('Fileira onde o equipamento está localizado é obrigatória.')",
                'oninput': "this.setCustomValidity('')",
            }),
            'fabricante': forms.TextInput(attrs={
                'placeholder': 'Fabricante',
                'maxlength': '50',
                }),
            'data_aquisicao': forms.DateInput(attrs={
                'type': 'date',
                'oninvalid': "this.setCustomValidity('Data de aquisição é obrigatória.')",
                'oninput': "this.setCustomValidity('')",
            })
        }

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['email', 'email_escolar', 'cpf', 'numero', 'password', 'groups']
        labels = {
            'groups': 'Tipo de Usuario'
        }

        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'oninvalid': "this.setCustomValidity('Email é obrigatório.')",
                'oninput': "this.setCustomValidity('')",
                'placeholder':'exemplo@gmail.com',
                'maxlength':'100',
            }),
            'email_escolar': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@escolar.com',
                'oninvalid': "this.setCustomValidity('Email escolar é obrigatório.')",
                'oninput': "this.setCustomValidity('')",
                'maxlength':'100',
            }),
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000',
                'oninvalid': "this.setCustomValidity('Número de telefone é obrigatório.')",
                'oninput': "this.setCustomValidity('')",
                'maxlength':'11',
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00',
                'oninvalid': "this.setCustomValidity('CPF é obrigatório.')",
                'oninput': "this.setCustomValidity('')",
                'maxlength':'11',   
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Digite a senha',
                'oninvalid': "this.setCustomValidity('Senha é obrigatória.')",
                'oninput': "this.setCustomValidity('')",
                'maxlength':'30',
            }),
            'groups': forms.CheckboxSelectMultiple(attrs={
                'oninvalid': "this.setCustomValidity('Nivel de acesso é obrigatório.')",
                'oninput': "this.setCustomValidity('')",
            }),
        }