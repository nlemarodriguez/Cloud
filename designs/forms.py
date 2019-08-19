from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Company


class CustomUserCreationForm(UserCreationForm):
    password = None
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Direccion email'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Crear contrasena', 'type': 'password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repetir contrasena', 'type': "password"})


class CompanyCreationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de la compania'})
