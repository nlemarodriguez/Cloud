import time
import os
import django
from datetime import datetime
import requests
from PIL import Image, ImageDraw
from rest_framework.utils import json
from django.conf import settings
from random import randint
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_1.settings")
django.setup()
from designs.models import Company, Project, Design, State


count = Design.objects.filter(process_file='').count()-1
random = randint(0, count)
design = Design.objects.filter(process_file='')[count]
while design:
    design.process_file = '.'
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
    if Design.objects.filter(process_file=''):
        count = Design.objects.filter(process_file='').count() - 1
        random = randint(0, count)
        design = Design.objects.filter(process_file='')[count]
    else:
        design = None