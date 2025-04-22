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
- **Pytest + Coverage**
- **scikit-learn** (IA de categorización de gastos)

---

## 🔧 Configuración rápida

1. Clona el repositorio:

```bash
git clone https://github.com/AlbertClemente/zenkoo-backend.git
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

---

### 👤 Usuarios por defecto

Se crean automáticamente:

#### 🔑 Administrador
- Email: `admin@zenkoo.com`
- Password: `ZenkooSuper2025!`

#### 👤 Usuario de test
- Email: `test2.user@zenkoo.com`
- Password: `clave123`

#### ⚙️ Usuario del cron de CoinGecko
- Email: `cronjob@zenkoo.com`

> Puedes cambiarlas en `.env` o en el script de creación automática.

---

## 🔐 Endpoints de Autenticación

- Registro: POST /api/users/register/
- Login (JWT): POST /api/users/login/

Usa el access token en las llamadas autenticadas:

```bash
Authorization: Bearer <access_token>
```

---

## 📚 Documentación API

Zenkoo ofrece documentación Swagger generada con DRF Spectacular:

🔗 [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)

Incluye:
- Esquema OpenAPI completo (`Zenkoo API.yaml`)
- Ejemplos de respuesta (200, 201, 400, 403...)
- WebSocket documentado

---

## 🧪 Ejecutar tests

```bash
docker-compose exec web pytest
```

Y para ver la cobertura:

```bash
docker-compose exec web pytest --cov=savings --cov-report=term-missing
```

---

## 🌐 WebSocket en tiempo real

- URL: `ws://localhost:8000/ws/criptos/`
- Se emiten actualizaciones si el precio cambia más de un 1%.

Ejemplo de payload:

```json
{
  "type": "update_price",
  "payload": {
    "symbol": "BTC",
    "price": 65234.21,
    "timestamp": "2025-04-22T16:00:00Z"
  }
}
```

---

## 🤖 Categorización automática con IA

Zenkoo usa **Naive Bayes** + **TfidfVectorizer** con `scikit-learn`.

- Entrena desde la base de datos
- Guarda modelo en `static/ml/model.pkl`
- Consulta:
  - `GET /api/admin/model-info/`
  - `POST /api/admin/retrain/`

Accesible solo para `is_staff=True`.

---

## 📦 Exportar imágenes Docker

```bash
docker save -o zenkoo-backend.tar zenkoo-backend
docker save -o zenkoo-frontend.tar zenkoo-frontend
```

---

## 🧪 Ejecutar cron manualmente

```bash
docker-compose exec \
  -e LOGIN_URL=http://localhost:8000/api/users/login/ \
  -e UPDATE_URL=http://localhost:8000/api/criptos/update/ \
  backend python cron_update_criptos.py
```

---

## 📂 Estructura del proyecto

```bash
zenkoo-backend/
├── backend/               # Configuración Django
├── savings/               # App principal (modelos, views, etc.)
├── staticfiles/           # Archivos estáticos recolectados
├── cron_update_criptos.py # Script del cron
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── .env / .env.example
├── manage.py
├── requirements.txt
├── Zenkoo API.yaml
└── README.md
```

---

## 🧑‍💻 Autor

Desarrollado por [Albert Clemente](https://github.com/AlbertClemente) como proyecto final del CFGS de Desarrollo de Aplicaciones Web en [Ilerna](https://www.ilerna.es/).

> 🇪🇸 Este README está en español. [Switch to English](README.en.md) _(coming soon)_
