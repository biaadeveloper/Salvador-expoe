from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import PerfilUsuario


class CadastroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Informe sua data de nascimento'
    )
    aceita_localizacao = forms.BooleanField(
        required=False,
        label='Permitir uso da minha localização',
        help_text='Marque esta opção para permitir que o site utilize sua localização'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=True)

        perfil = PerfilUsuario(
            usuario=user,
            data_nascimento=self.cleaned_data['data_nascimento'],
            aceita_localizacao=self.cleaned_data['aceita_localizacao']
        )

        if commit:
            perfil.save()

        return user
