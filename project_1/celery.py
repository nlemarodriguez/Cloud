from __future__ import absolute_import, unicode_literals
import os
import django
from celery import Celery
from project_1 import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_1.settings")
django.setup()
from PIL import Image, ImageDraw
from django.core.files import File
from io import BytesIO
from designs.models import Company, Project, Design, State
import boto3
from botocore.exceptions import ClientError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

sqs = boto3.client('sqs', region_name='us-east-1')
queue_url = settings.AWS_QUEUE_URL

app = Celery('project_1', broker=settings.BROKER_URL)
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()


# app.conf.beat_schedule = {
#     'display_time-30-seconds': {
#         'task': 'demoapp.tasks.display_time',
#         'schedule': 10.0
#     },
# }


@app.task(bind=True)
def debug_task():
    # print('Request: {0!r}'.format(self.request))
    try:
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
    except ClientError as e:
        response = None

    if response is not None:
        try:
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
            draw.text((20, height - 30),
                      'Diseñador: {} {}\nFecha: {}'.format(design.designer_name, design.designer_last_name
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

            message = Mail(
                from_email=settings.EMAIL_DESIGN_USER,
                to_emails=design.designer_email,
                subject='Diseño procesado',
                html_content='<p>Tu diseño ha sido procesado! <br><br> Ahora es visible para todos: '
                             '<a href=http://entrega4-grupo01.herokuapp.com/empresas/' + design.project.company.url +
                             '> Ver proyecto </a> </p>')

            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
            print(response.status_code, response.body, response.headers)

            # Delete received message from queue
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
        except KeyError:
            pass
        except Exception:
            pass
