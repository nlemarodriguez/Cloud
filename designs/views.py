from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.utils import json

from .forms import CustomUserCreationForm, CompanyCreationForm, ProjectCreationForm, DesignCreationForm
from .models import Company, Project, Design, State
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils.text import slugify
from django.http import HttpResponse, Http404
import os
from django.conf import settings
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import boto3
import requests


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


# Es la empresa particular, solo cuando no ha seleccionado un proyecto
def empresa(request, url):
    print('url: ' + url)
    company = Company.objects.get(url=url)
    projects = Project.objects.filter(company=company)
    return render(request, 'designs/empresa.html', {'company': company, 'projects': projects, 'cloud_front': settings.CLOUD_FRONT_URL})


# Recibe el proyecto y la empresa
def proyecto(request, url, idproyecto):
    company = Company.objects.get(url=url)
    projects = Project.objects.filter(company=company)
    project = Project.objects.get(id=idproyecto)
    designs_list = Design.objects.filter(project=project).order_by('-created_date')
    paginator = Paginator(designs_list, 10)  # Show 10 designs per page
    page = request.GET.get('page')
    designs_owner = paginator.get_page(page)
    state_design, created = State.objects.get_or_create(name='Disponible')
    designs_list_d = Design.objects.filter(project=project, state=state_design).order_by('-created_date')
    paginator2 = Paginator(designs_list_d, 10)  # Show 10 designs per page
    page2 = request.GET.get('page')
    designs_designer = paginator2.get_page(page2)
    design_form = DesignCreationForm()
    if request.method == 'POST':
        form_project = ProjectCreationForm(request.POST, instance=project)
        if form_project.is_valid():
            form_project.save()
            messages.success(request, 'Proyecto actualizado con éxito')
            return empresa(request, url)
        else:
            print('paila actualizando')
    else:
        form_project = ProjectCreationForm(instance=project)
        return render(request, 'designs/empresa.html',
                      {'form_project': form_project, 'company': project.company, 'designs_owner': designs_owner,
                       'designs_designer': designs_designer, 'projects': projects, 'project': project,
                       'design_form': design_form, 'cloud_front': settings.CLOUD_FRONT_URL})


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
            messages.success(request, 'Proyecto creado con éxito')
            return empresa(request, url)
        else:
            print('paila proyecto')
    else:
        form_project = ProjectCreationForm()
        return render(request, 'designs/empresa.html',
                      {'form_project': form_project, 'company': company, 'projects': projects, 'cloud_front': settings.CLOUD_FRONT_URL})


@csrf_exempt
def nuevo_design(request, url, idproyecto):
    print(request)
    # print(request.body)
    print(request.POST)
    if request.method == 'POST':
        form_design = DesignCreationForm(request.POST, request.FILES)
        if form_design.is_valid():
            design = form_design.save(commit=False)
            state, created = State.objects.get_or_create(name='En proceso')
            design.state = state
            project = Project.objects.get(id=idproyecto)
            design.project = project
            design.save()
            sqs = boto3.resource('sqs', region_name='us-east-1')
            queue = sqs.get_queue_by_name(QueueName=os.environ["AWS_QUEUE_NAME"])
            response = queue.send_message(MessageBody='Id design to process', MessageAttributes={
                'Id': {
                    'StringValue': str(design.id),
                    'DataType': 'Number'
                }
            })

            print('response: '+response['MessageId'])
            request.method = 'GET'
            messages.info(request,
                          'Hemos recibido tu diseño y lo estamos procesado para que sea publicado. Tan pronto esto ocurra, te notificaremos por email')
            return proyecto(request, url, idproyecto)
        else:
            print(form_design.errors)
            # return proyecto(request, url, idproyecto)
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
            messages.error(request, 'Correo y contraseña incorrectos!')
            return redirect('home')


def dowload_image(request, tipo, id):
    design = Design.objects.get(id=id)
    if tipo == 'original':
        file_path = settings.CLOUD_FRONT_URL + '/' + str(design.original_file)
    else:
        file_path = settings.CLOUD_FRONT_URL + '/' + str(design.process_file)
    print(file_path)

    # r = requests.get(file_path)  # create HTTP response object
    # with open("python_logo.png", 'wb') as f:
    #     f.write(r.content)

    # with open(file_path, 'wb') as fh:
    #     response = HttpResponse(fh.read(), content_type="application/")
    #     response['Content-Disposition'] = 'inline; filename=' + file_path
    #     return response


# Trae todos los diseños con estado 'En proceso'
@api_view(['GET'])
def get_designs(request):
    status, created = State.objects.get_or_create(name='En proceso')

    try:
        design = Design.objects.filter(state=status)
    except Design.DoesNotExist:
        raise NotFound(detail="Error 404, No designs in process", code=404)

    designs = []

    for des in design:
        designs.append({"id": des.pk, "designer_name": des.designer_name, "designer_last_name": des.designer_last_name,
                        "created_date": str(des.created_date), "original_file": str(des.original_file)})
    return HttpResponse(json.dumps(designs), content_type="application/json")


# Se actualiza el estado del diseño y la ruta del archivo procesado
@api_view(['PUT'])
def put_designs(request):
    dis = json.loads(request.body.decode('utf-8'))

    try:
        design = Design.objects.get(pk=dis['id'])
    except Design.DoesNotExist:
        raise NotFound(detail="Error 404, Design not found", code=404)

    status, created = State.objects.get_or_create(name='Disponible')

    design.state = status
    design.process_file = dis['process_file']
    design.save()

    send_email_designer(design.designer_email)

    designs_process = [{"designer_name": design.designer_name, "designer_last_name": design.designer_last_name,
                        "created_date": str(design.created_date), "original_file": str(design.original_file),
                        "process_file": str(design.process_file), "state": str(design.state.name)}]

    return HttpResponse(json.dumps(designs_process), content_type="application/json")


def send_email_designer(mail_designer):
    send_mail('Diseño procesado', 'Tu diseño ha sido procesado! Ahora es visible para todos',
              os.environ["EMAIL_DESIGN_USER"], [mail_designer])


def update_url(request):
    if request.method == 'POST':
        pk_company = request.POST.get('company_pk')
        url_company = request.POST.get('company_url')
        company_list = Company.objects.filter(url=url_company)
        if len(company_list) > 0:
            messages.error(request, 'ERROR! Esa Url ya existe, intente con una nueva')
            return redirect('empresas')
        else:
            company = Company.objects.get(pk=pk_company)
            company.url = slugify(url_company)
            company.save()
            return redirect('empresas')


def upload_design(request):
    try:
        project = Project.objects.filter(name='Dia de la mujer')
        state = State.objects.filter(name='En proceso')
        design = Design(value=1, designer_email='1@1.com', designer_last_name='apellido', designer_name='nombre',
                        original_file='original/imagen-consciencia.jpg', state=state[0], project=project[0])
        design.save()
        return HttpResponse(status=204)
    except Exception:
        return HttpResponse(status=500)

