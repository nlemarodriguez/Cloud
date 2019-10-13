import time
import os
import django
from PIL import Image, ImageDraw
from django.core.files import File
from io import BytesIO
from random import randint
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_1.settings")
django.setup()
from django.core.mail import send_mail
from designs.models import Company, Project, Design, State
import boto3

sqs = boto3.client('sqs', region_name='us-east-1')
queue_url = 'https://sqs.us-east-1.amazonaws.com/155149968057/modeloD-Cola'


while True:

    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )

    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']

    id = message['MessageAttributes']['Id']['StringValue']
    design = Design.objects.get(id=int(id))

    desired_size = 800
    img = Image.open(design.original_file)

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
    status, created = State.objects.get_or_create(name='Disponible')
    process_url = filename + '.png'
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    file_object = File(buffer)
    file_object.content_type = 'image/png'

    design.process_file.save(process_url, file_object)
    design.state = status
    design.save()
    send_mail('Diseño procesado', 'Tu diseño ha sido procesado! Ahora es visible para todos', os.environ["EMAIL_DESIGN_USER"], [design.designer_email])
    # Delete received message from queue
    sqs.delete_message(
         QueueUrl=queue_url,
         ReceiptHandle=receipt_handle
     )
    time.sleep(10)


