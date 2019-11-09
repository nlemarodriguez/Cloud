from celery import Celery
from hirefire.procs.celery import CeleryProc
from project_1 import settings

#celery = Celery('project_1', broker=settings.BROKER_URL, backend=settings.BROKER_BACKEND+'://')

class WorkerProc(CeleryProc):
    name = 'worker'
    queues = ['celery']
 #   app = celery