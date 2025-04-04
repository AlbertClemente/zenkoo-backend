# 💸 Zenkoo - App de Ahorro Personal

Zenkoo es una aplicación web para gestionar tus finanzas personales, basada en el método **Kakeibo**. Permite registrar ingresos, gastos, metas de ahorro y reflexiones personales. Además, integra precios en tiempo real de criptomonedas populares (BTC, ETH, USDT) mediante CoinGecko y WebSockets.

🧠 Proyecto final del **Ciclo Formativo de Grado Superior en Desarrollo de Aplicaciones Web** (DAW) en Ilerna.

🔗 [Repositorio del frontend](https://github.com/AlbertClemente/zenkoo-frontend)

---

## 🛠️ Tecnologías utilizadas

- **Django** + **Django REST Framework** (API REST)
- **DRF Spectacular** (Documentación OpenAPI / Swagger)
- **PostgreSQL** (BD relacional con UUID como PK)
- **Docker** + **docker-compose** (contenedores)
- **Gunicorn** + **Uvicorn** (servidor WSGI/ASGI)
- **Django Channels** + **Daphne** (WebSockets en producción)

---

## 🔧 Configuración rápida

1. Clona el repositorio:

```bash
git clone https://github.com/tuusuario/zenkoo-backend.git
cd zenkoo-backend
```

2. Crea un archivo .env:

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

## 👤 Superusuario por defecto

Al iniciar, se crea automáticamente un usuario administrador con las siguientes credenciales por defecto (configurables por entorno):

- Email: admin@zenkoo.com
- Password: ZenkooSuper2025!

Puedes cambiarlos modificando las variables en el .env o en el script de creación automática.

## 📚 Documentación API

Zenkoo cuenta con documentación completa mediante Swagger y drf-spectacular, incluyendo:

- Ejemplos de respuesta (200, 201, 204)
- Errores comunes (400, 401, 403, 404)
- WebSocket documentado para precios en tiempo real

## 🧪 Ejecutar tests

```bash
docker-compose exec web python manage.py test
```

## 📂 Estructura del proyecto

```bash
zenkoo-backend/
│
├── backend/                # Configuración principal del proyecto Django
├── savings/                # App principal: modelos, vistas, serializers, lógica
├── staticfiles/            # Archivos estáticos recopilados
├── docker-compose.yml      # Orquestación de servicios con Docker
├── Dockerfile              # Imagen del backend con Daphne, Uvicorn y Gunicorn
├── .env                    # Variables de entorno (excluidas del repo)
├── requirements.txt        # Dependencias de Python
├── API_Zenkoo.md           # Documentación manual de la API
└── README.md               # Este archivo
```
## 🌐 WebSocket en tiempo real

Zenkoo actualiza automáticamente los precios de BTC, ETH y USDT cada vez que se llama al endpoint /api/criptos/update/, enviando el nuevo precio a través del canal WebSocket:

```bash
ws://localhost:8000/ws/criptos/
```
