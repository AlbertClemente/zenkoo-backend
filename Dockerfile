# Dockerfile

# Imagen base oficial de Python, versión 3.13 con variante slim (más ligera)
FROM python:3.13-slim

# Evita crear archivos .pyc (bytecode) innecesarios
ENV PYTHONDONTWRITEBYTECODE=1

# Hace que los logs de Python se impriman directamente al terminal (sin buffering)
ENV PYTHONUNBUFFERED=1

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias (requirements.txt) de nuestro backend al contenedor
COPY requirements.txt .

# Actualiza pip y luego instala las dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia todo el código del backend al contenedor en /app
COPY . .

# Comando por defecto al arrancar el contenedor
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]

# Copia el entrypoint al contenedor
COPY entrypoint.sh /entrypoint.sh

# Da permisos de ejecución
RUN chmod +x /entrypoint.sh

# Usa el script como comando por defecto
ENTRYPOINT ["/entrypoint.sh"]