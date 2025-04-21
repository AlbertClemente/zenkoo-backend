FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala cron y dependencias para Pillow o similares
RUN apt-get update && apt-get install -y cron build-essential libpq-dev

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Recolecta los archivos estáticos
RUN python manage.py collectstatic --noinput

# Copia el entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Configura cron
COPY crontabfile /etc/cron.d/zenkoo-cron
RUN chmod 0644 /etc/cron.d/zenkoo-cron && crontab /etc/cron.d/zenkoo-cron

ENTRYPOINT ["/entrypoint.sh"]
#CMD ["gunicorn", "backend.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "backend.asgi:application"]
