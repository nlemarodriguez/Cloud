from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm, CompanyCreationForm, ProjectCreationForm, DesignCreationForm
from .models import Company, Project, Design, State
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils.text import slugify


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


# Es el link del navbar que devuelve todas las empresas
def empresas(request):
    companies = Company.objects.all().order_by('-name')
    return render(request, 'designs/empresas.html', {'companies': companies})


# Es la empresa particualar, solo cuando no ha seleccionado un proyecto
def empresa(request, url):
    print('url: ' + url)
    company = Company.objects.get(url=url)
    projects = Project.objects.filter(company=company)
    return render(request, 'designs/empresa.html', {'company': company, 'projects': projects})


# Recibe el proyecto y la empresa
def proyecto(request, url, idproyecto):
    company = Company.objects.get(url=url)
    projects = Project.objects.filter(company=company)
    project = Project.objects.get(id=idproyecto)
    designs = Design.objects.filter(project=project)
    design_form = DesignCreationForm()
    if request.method == 'POST':
        form_project = ProjectCreationForm(request.POST, instance=project)
        if form_project.is_valid():
            form_project.save()
            messages.success(request, 'Proyecto actualizado con exito')
            return empresa(request, url)
        else:
            print('paila actualizando')
    else:
        form_project = ProjectCreationForm(instance=project)
        return render(request, 'designs/empresa.html',
                      {'form_project': form_project, 'company': project.company, 'designs': designs,
                       'projects': projects, 'project': project, 'design_form': design_form})


def eliminar_proyecto(request, url, idproyecto):
    Project.objects.get(id=idproyecto).delete()
    return empresa(request, url)


def nuevo_proyecto(request, url):
    company = Company.objects.get(url=url)
    projects = Project.objects.filter(company=company)
    if request.method == 'POST':
        form_project = ProjectCreationForm(request.POST)
        if form_project.is_valid():
            project = form_project.save(commit=False)
            company = Company.objects.get(url=url)
            project.company = company
            project.save()
            messages.success(request, 'Proyecto creado con exito')
            return empresa(request, url)
        else:
            print('paila proyecto')
    else:
        form_project = ProjectCreationForm()
        return render(request, 'designs/empresa.html',
                      {'form_project': form_project, 'company': company, 'projects': projects})


def nuevo_design(request, url, idproyecto):
    if request.method == 'POST':
        print('1')
        form_design = DesignCreationForm(request.POST, request.FILES)
        if form_design.is_valid():
            print('1')
            design = form_design.save(commit=False)
            state, created = State.objects.get_or_create(name='En proceso')
            design.state = state
            project = Project.objects.get(id=idproyecto)
            design.project=project
            design.save()
            request.method='GET'
            return proyecto(request, url, idproyecto)
        else:
            print('paila diseno')
            print(form_design.errors)
            #return proyecto(request, url, idproyecto)
    else:
        pass

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
            # Decidi usar el concecutivo con el id de la compania
            company.url = slugify(form_company.cleaned_data['name']) + str(company.id)
            company.save()
            return redirect('home')
        else:
            print('paila')
            # print('user errors: ' + form_user.__str__())
            # print('company errors: ' + form_company.__str__())
    else:
        form_user = CustomUserCreationForm()
        form_company = CompanyCreationForm()
        # print(form_user)
        # print(form_company)
    return render(request, 'designs/registro.html', {'form_user': form_user, 'form_company': form_company})


def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            company = Company.objects.get(owner=user)
            return empresa(request, company.url)
        else:
            pass