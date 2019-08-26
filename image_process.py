import requests
from PIL import Image, ImageDraw

# Consulta las imagenes sin procesar
from rest_framework.utils import json

url = 'http://127.0.0.1:8000/disenos/'

response = requests.get(url)
designs = json.loads(response.text)

# Se recorre el json con las imagenes sin procesar
for i in designs:

    desired_size = 800

    img = Image.open('../media/{}'.format(i['original_file']))

    # Se ajusta tamaño de la imagen
    old_size = img.size
    ratio = float(desired_size)/max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])
    img = img.resize(new_size, Image.ANTIALIAS)

    # se comenta la imagen con el nombre del diseñador y fecha
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), 'Diseñador: {} {}\nFecha: {}'.format(i['designer_name'], i['designer_last_name']
                                                              , i['created_date']), fill="white")

    # Obtener nombre de archivo
    file = '{}'.format(i['original_file'])
    position = file.index('.')
    filename = file[9:position]

    # Se guarda nueva imagen
    img.save('../media/process/' + filename + '.png')
