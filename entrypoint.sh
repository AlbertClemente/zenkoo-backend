#!/bin/bash

# Espera a que el contenedor de la base de datos esté listo
echo "Esperando a que la base de datos esté disponible..."
python manage.py wait_for_db

# Aplica migraciones
echo "Aplicando migraciones..."
python manage.py migrate

# Recolecta los archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Setea el Superadmin
echo "Seteando Superadmin para Django..."
python manage.py create_default_superuser

# Ejecuta el servidor (gunicorn)
echo "Iniciando Gunicorn..."
exec gunicorn backend.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000