import time
import os
import django
from datetime import datetime
import requests
from PIL import Image, ImageDraw
from boto.ses.exceptions import SESDailyQuotaExceededError
from rest_framework.utils import json
from django.conf import settings
from random import randint
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_1.settings")
django.setup()
from django.core.mail import send_mail
from designs.models import Company, Project, Design, State


def return_any_design():
    contador = Design.objects.filter(process_file='').count()
    if contador==0:
        return None
    elif contador==1:
        return Design.objects.filter(process_file='')[0]
    else:
        random = randint(0, contador - 1)
        return Design.objects.filter(process_file='')[random]

design = return_any_design()

while design:
    design.process_file = '.'
    design.save()
    desired_size = 800
    img = Image.open(settings.MEDIA_ROOT + '/{}'.format(design.original_file))

    # Se ajusta tamaño de la imagen
    old_size = img.size
    ratio = float(desired_size) / max(old_size)
    new_size = tuple([int(x * ratio) for x in old_size])
    img = img.resize(new_size, Image.ANTIALIAS)

    width, height = img.size

    # se comenta la imagen con el nombre del diseñador y fecha
    draw = ImageDraw.Draw(img)
    draw.text((20, height - 30), 'Diseñador: {} {}\nFecha: {}'.format(design.designer_name, design.designer_last_name
                                                                      , design.created_date), fill="white")

    # Obtener nombre de archivo
    file = '{}'.format(design.original_file)
    position = file.index('.')
    filename = file[9:position]
    print(filename)
    # Se guarda nueva imagen
    img.save(settings.MEDIA_ROOT + '/process/' + filename + '.png')

    status, created = State.objects.get_or_create(name='Disponible')

    design.process_file = 'process/' + filename + '.png'
    design.state = status
    design.save()
    try:
        send_mail('Diseño procesado', 'Tu diseño ha sido procesado! Ahora es visible para todos', os.environ["EMAIL_DESIGN_USER"], [design.designer_email])
    except SESDailyQuotaExceededError:
        print('capturo error')
    design = return_any_design()

