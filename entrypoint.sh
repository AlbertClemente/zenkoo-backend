#!/bin/bash

echo "Esperando a que la base de datos esté disponible..."
python manage.py wait_for_db

# echo "Creando migraciones..."
# python manage.py makemigrations --noinput

echo "Aplicando migraciones..."
python manage.py migrate

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Seteando Superadmin para Django..."
python manage.py create_default_superuser

echo "Seteando usuario para cron (ZENKOO_CRON_EMAIL)..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
email = "${ZENKOO_CRON_EMAIL}"
password = "${ZENKOO_CRON_PASSWORD}"
profile_picture = "https://example.com/avatar.png"
date_of_birth = "1900-01-01"

if not User.objects.filter(email=email).exists():
    print("Creando usuario cron...")
    User.objects.create_user(email=email, password=password, profile_picture=profile_picture, date_of_birth=date_of_birth, is_active=True)
else:
    print("Usuario cron ya existe.")
EOF

echo "Entrenando modelo Kakeibo inicial..."
python manage.py shell -c "from savings.ml.train import train_model; train_model()"

echo "Iniciando cron..."
cron

# Ejecuta el proceso principal (gunicorn en este caso)
exec "$@"