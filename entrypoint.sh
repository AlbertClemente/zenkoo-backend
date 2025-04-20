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

echo "Seteando usuario de test si no existe..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
email = "${ZENKOO_USER_TEST_EMAIL}"
password = "${ZENKOO_USER_TEST_PASSWORD}"
profile_picture = "https://example.com/avatar.png"
date_of_birth = "1990-01-01"

if not User.objects.filter(email=email).exists():
    print("Creando usuario de test...")
    User.objects.create_user(email=email, password=password, profile_picture=profile_picture, date_of_birth=date_of_birth, is_active=True)
else:
    print("Usuario de test ya existe.")
EOF

echo "Insertando categorías predeterminadas si no existen..."
python manage.py shell << EOF
from savings.models import Category
from django.contrib.auth import get_user_model

# Obtener el usuario test por su email
user = get_user_model().objects.filter(email="${ZENKOO_USER_TEST_EMAIL}").first()

if not user:
    print("No se encontró el usuario de test. Creando usuario cron...")
    user = get_user_model().objects.create_user(
        email="${ZENKOO_USER_TEST_EMAIL}",
        password="${ZENKOO_USER_TEST_PASSWORD}",
        profile_picture="https://example.com/avatar.png",
        date_of_birth="1900-01-01",
        is_active=True
    )

# Categorías predeterminadas
categories = ["Supervivencia", "Ocio y vicio", "Cultura", "Extras"]

# Crear categorías si no existen
for category_name in categories:
    Category.objects.get_or_create(name=category_name, type="expense", user=user)

print("Categorías predeterminadas insertadas para el usuario cron.")
EOF

echo "Entrenando modelo Kakeibo inicial si no existe..."
python manage.py shell << EOF
import os
from savings.ml.train import train_model

# Ruta donde se guarda el modelo
model_path = '/app/savings/static/ml/model.pkl'

# Verificar si el modelo ya existe
if not os.path.exists(model_path):
    print("Modelo no encontrado, entrenando modelo Kakeibo...")
    train_model()  # Llamar a tu función para entrenar el modelo
else:
    print("El modelo ya está entrenado.")
EOF

echo "Iniciando cron..."
cron

# Ejecuta el proceso principal (gunicorn en este caso)
echo "🚀 Lanzando servidor..."
exec "$@"