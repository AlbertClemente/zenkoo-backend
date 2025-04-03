# 💸 Zenkoo - App de Ahorro Personal

Zenkoo es una aplicación web para gestionar tus finanzas personales, siguiendo el método **Kakeibo** y con integración básica de criptomonedas. Desarrollada como proyecto final del CFGS DAW en Ilerna.

🔗 [Repositorio del frontend](https://github.com/AlbertClemente/zenkoo-frontend)

## 🛠️ Tecnologías

- Backend: **Django + Django REST Framework**
- Base de datos: **PostgreSQL**
- Contenedores: **Docker + docker-compose**
- Otros: **Gunicorn**, **Uvicorn**, **ASGI**, **WebSockets**

## 🚀 Requisitos

- Docker
- Docker Compose

## 🔧 Configuración

1. Clona el repositorio:

```bash
git clone https://github.com/tuusuario/zenkoo-backend.git
cd zenkoo-backend
```

2. Clona el repositorio:

```bash
POSTGRES_DB=zenkoo
POSTGRES_USER=zenkoo
POSTGRES_PASSWORD=zenkoo
POSTGRES_PORT=5432
DJANGO_SECRET_KEY=changeme
DJANGO_DEBUG=True
```

3. Levanta los contenedores Docker:

```bash
docker-compose up --build
```
El backend estará disponible en http://localhost:8000.

## 👤 Superusuario

Al iniciar, se crea automáticamente un usuario administrador con las siguientes credenciales por defecto (configurables por entorno):

- Email: admin@zenkoo.com
- Password: ZenkooSuper2025!

Puedes cambiarlos modificando las variables en el .env o en el script de creación automática.

## 🧪 Tests

```bash
docker-compose exec web python manage.py test
```

## 📂 Estructura básica

```bash
zenkoo-backend/
│
├── backend/                # Configuración principal de Django
├── savings/                # App principal: usuarios, gastos, ingresos, ahorro
├── staticfiles/            # Archivos estáticos recogidos
├── Dockerfile              # Imagen del backend
├── docker-compose.yml      # Orquestación de servicios
├── requirements.txt        # Archivo con los paquetes necesarios para el backend / Docker
└── .env                    # Variables de entorno (no subidos al repo)
```