from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Company, Project, Design


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


class ProjectCreationForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'cost')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre del proyecto'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Descripcion del proyecto'})
        self.fields['cost'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Costo del proyecto'})


class DesignCreationForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = ('value', 'original_file', 'designer_name', 'designer_last_name', 'designer_email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['value'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Valor del diseno'})
        self.fields['designer_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Nombre del disenador'})
        self.fields['designer_last_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Apellido del disenador'})
        self.fields['designer_email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Email del disenador'})
