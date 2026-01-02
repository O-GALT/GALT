from django import forms
from core.essenciais import TipoUsuario
from locais.models import Predio, Setor, PredioSetor, Sala
from contas.models import Usuario
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
        model = Usuario
        fields = ['username', 'email_pessoal', 'email_escolar', 'cpf', 'telefone', 'tipo_usuario', 'password']
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
            'email_pessoal': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@pessoal.com'}),
            'email_escolar': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@escolar.com'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(99) 12345-6789'}),
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
