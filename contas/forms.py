from django import forms
from core.essenciais import TipoUsuario
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
        fields = ['setor']
        labels = {
            'setor': 'Nome do Setor',
        }
        widgets = {
            'setor': forms.TextInput(attrs={'class': '', 'placeholder': 'Setor A'}),
        }

class SalaForm(forms.ModelForm):
    class Meta:
        model = Salas
        fields = ['estado_atual', 'localizacao', 'setor']
        widgets = {
            'estado_atual': forms.Select(attrs={'class': ''}),
            'localizacao': forms.TextInput(attrs={'class': '', 'placeholder': 'Primeiro andar'}),
            'setor': forms.Select(attrs={'class': ''})
        }

class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamentos
        fields = ['tipo', 'serial', 'posicao', 'estado_equipamento', 'sala']
        widgets = {
            'tipo': forms.Select(attrs={'class': ''}),
            'serial': forms.NumberInput(attrs={'class': '', 'placeholder': '123456'}),
            'posicao': forms.TextInput(attrs={'class': '', 'placeholder': 'Posição'}),
            'estado_equipamento': forms.Select(attrs={'class': ''}),
            'sala': forms.Select(attrs={'class': ''}),
            'fabricante': forms.TextInput(attrs={'class': '', 'placeholder': 'Fabricante'}),
            'data_aquisicao': forms.DateInput(attrs={'class': '', 'placeholder': 'Data de Aquisição'})
        }

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label='Senha', 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite a senha'})
    )
    
    confirm_password = forms.CharField(
        label='Confirme a Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repita a senha'})
    )

    class Meta:
        model = Usuarios
        fields = ['username', 'email', 'email_escolar', 'cpf', 'tipo_usuario', 'password']
        
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'exemplo@gmail.com'}),
            'email_escolar': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@escolar.com'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("password")
        confirmacao = cleaned_data.get("confirm_password")

        if senha and confirmacao and senha != confirmacao:
            raise forms.ValidationError("As senhas não conferem!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
