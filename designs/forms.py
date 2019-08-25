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
        self.fields['name'].label = 'Nombre'
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre del proyecto', 'title':'Nombre'})
        self.fields['description'].label = 'Descripción'
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Descripcion del proyecto'})
        self.fields['cost'].label = 'Costo'
        self.fields['cost'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Costo del proyecto'})


class DesignCreationForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = ('value', 'original_file', 'designer_name', 'designer_last_name', 'designer_email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['original_file'].label = 'Diseño'
        self.fields['original_file'].widget.attrs.update({'class': 'form-control'})
        self.fields['value'].label = 'Valor del diseño'
        self.fields['value'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Valor del diseño'})
        self.fields['designer_name'].label = 'Nombre del diseñador'
        self.fields['designer_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Nombre del diseñador'})
        self.fields['designer_last_name'].label = 'Apellido del diseñador'
        self.fields['designer_last_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Apellido del diseñador'})
        self.fields['designer_email'].label = 'Email del diseñador'
        self.fields['designer_email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Email del diseñador'})
