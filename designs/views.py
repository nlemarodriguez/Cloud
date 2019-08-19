from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm, CompanyCreationForm
from .models import Company, Project
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
# Create your views here.

def home(request):
    if request.user is not None:
        # Redirect to a success page.
        print('1')
        return render(request, 'designs/home.html')
    else:
        # Return an 'invalid login' error message.
        print('2')
        return render(request, 'designs/home.html')


#Es el link del navbar que devuelve todas las empresas
def empresas(request):
    companies = Company.objects.all().order_by('-name')
    return render(request, 'designs/empresas.html', {'companies': companies})


#Es la empresa particualar, solo cuando no ha seleccionado un proyecto
def empresa(request, url):
    print('url: '+ url)
    company = Company.objects.filter(url=url)
    projects = Project.objects.filter(company=company)
    #Se debe consultar la empresa y mandarle los datos al template con el primer proyecto
    return render(request, 'designs/empresa.html')


#Recibe el proyecto y la empresa
def proyecto(request, url, proyecto):
    print('url: '+ url)
    print('proyecto: ' + proyecto)
    #Se debe consultar la empresa y mandarle los datos al template
    return render(request, 'designs/empresa.html')


def registro(request):
    if request.method == 'POST':
        form_user = CustomUserCreationForm(request.POST)
        form_company = CompanyCreationForm(request.POST)
        if form_user.is_valid() & form_company.is_valid():
            user = form_user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            company = form_company.save(commit=False)
            company.owner = user
            company.save()
            #Decidi usar el concecutivo con el id de la compania
            company.url = form_company.cleaned_data['name'] + str(company.id)
            company.save()
            return redirect('home')
        else:
            print('paila')
            #print('user errors: ' + form_user.__str__())
            #print('company errors: ' + form_company.__str__())
    else:
        form_user = CustomUserCreationForm()
        form_company = CompanyCreationForm()
        #print(form_user)
        #print(form_company)
    return render(request, 'designs/registro.html', {'form_user': form_user, 'form_company': form_company})