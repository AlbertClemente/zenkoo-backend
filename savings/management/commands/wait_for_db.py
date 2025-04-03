import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Espera a que la base de datos esté disponible'

    def handle(self, *args, **kwargs):
        self.stdout.write('Esperando a que la base de datos esté disponible...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
                db_conn.cursor()
            except OperationalError:
                self.stdout.write('Base de datos no disponible, esperando 1 segundo...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Base de datos disponible.'))