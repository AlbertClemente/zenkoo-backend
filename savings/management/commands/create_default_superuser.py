from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.timezone import now
import os

User = get_user_model()

class Command(BaseCommand):
    help = "Crea un superusuario si no existe"

    def handle(self, *args, **kwargs):
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@zenkoo.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'ZenkooSuper2025!')
        first_name = os.environ.get('DJANGO_SUPERUSER_FIRST_NAME', 'Admin')
        last_name = os.environ.get('DJANGO_SUPERUSER_LAST_NAME', 'Zenkoo')
        
        if not User.objects.filter(email=email).exists():
            self.stdout.write("Creando superusuario por defecto...")
            User.objects.create_superuser(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=now()
            )
            self.stdout.write(self.style.SUCCESS("Superusuario creado"))
        else:
            self.stdout.write(self.style.WARNING("Superusuario ya existe"))
