from datetime import datetime

import psycopg2

from django.conf import settings
import time
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_1.settings")
django.setup()
from designs.models import Design

while True:
    contador = Design.objects.filter(process_file='').count()
    f = open(settings.BASE_DIR + "/logs/log", "a+")
    now = datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S-%f')[:-3]
    f.write("Hora: %a -> Inicia conteo, cantidad de archivos por procesar: %a \r" % (
        now, contador))
    f.close()
    time.sleep(10)