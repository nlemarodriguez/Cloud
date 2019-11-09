from hirefire.procs.celery import CeleryProc

class WorkerProc(CeleryProc):
    name = 'worker'
    queues = ['celery']