import time
import os
import django
from datetime import datetime
import requests
from PIL import Image, ImageDraw
from rest_framework.utils import json
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_1.settings")
django.setup()

url = os.path.join(settings.MAIN_URL, 'disenos/')
url_update = os.path.join(settings.MAIN_URL, 'diseno-act/')

# Consulta las imagenes sin procesar
response = requests.get(url)
designs = json.loads(response.text)

# Se recorre el json con las imagenes sin procesar
f = open(settings.BASE_DIR + "/logs/log", "a+")
now = datetime.now()
f.write("Hora: %a -> Inicia proceso, cantidad de archivos a procesar: %a \r" % (
    now.strftime("%d/%m/%Y %H:%M:%S"), len(designs)))
for i in designs:
    now = datetime.now()
    f.write("Hora: %a -> Inicia conversion de archivo %a \r" % (
        now.strftime("%d/%m/%Y %H:%M:%S"), '{}'.format(i['original_file'])))
    desired_size = 800

    img = Image.open(settings.MEDIA_ROOT + '/{}'.format(i['original_file']))

    # Se ajusta tamaño de la imagen
    old_size = img.size
    ratio = float(desired_size) / max(old_size)
    new_size = tuple([int(x * ratio) for x in old_size])
    img = img.resize(new_size, Image.ANTIALIAS)

    width, height = img.size

    # se comenta la imagen con el nombre del diseñador y fecha
    draw = ImageDraw.Draw(img)
    draw.text((20, height - 30), 'Diseñador: {} {}\nFecha: {}'.format(i['designer_name'], i['designer_last_name']
                                                                      , i['created_date']), fill="white")

    # Obtener nombre de archivo
    file = '{}'.format(i['original_file'])
    position = file.index('.')
    filename = file[9:position]

    # Se guarda nueva imagen
    img.save(settings.MEDIA_ROOT + '/process/' + filename + now + '.png')

    # Se actualiza estado y ruta del diseño procesado
    data = {"original_file": '{}'.format(i['original_file']), "process_file": 'process/' + filename + '.png'}
    r = requests.put(url_update, data=json.dumps(data), timeout=10)

    # registro en log de eventos
    now = datetime.now()
    f.write("Hora: %a -> Convirtio archivo %a a archivo process/ %a .png \r" % (
        now.strftime("%d/%m/%Y %H:%M:%S"), '{}'.format(i['original_file']), filename))

f.write("Hora: %a -> Finaliza proceso \r\n" % (
    now.strftime("%d/%m/%Y %H:%M:%S")))
f.close()
