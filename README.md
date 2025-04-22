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

Al iniciar, se crean tres usuarios automáticamente: uno para el cron de CoinGecko, un administrador y un usuario de test. Las credenciales por defecto son:

#### 🔑 Administrador
- Email: `admin@zenkoo.com`
- Password: `ZenkooSuper2025!`

#### 👤 Usuario de test
- Email: `test2.user@zenkoo.com`
- Password: `clave123`

> Puedes cambiarlas en `.env` o en el script de creación automática.

---

## 🔐 Endpoints de Autenticación

- Registro: POST /api/users/register/
- Login (JWT): POST /api/users/login/

Recibirás un token access y refresh. Usa el access token para autenticarte con:

```bash
Authorization: Bearer <access_token>
```

---

## 📚 Documentación API

Zenkoo cuenta con documentación completa mediante Swagger y DRF-Spectacular, incluyendo:

- Ejemplos de respuesta (200, 201, 204)
- Errores comunes (400, 401, 403, 404)
- WebSocket documentado para precios en tiempo real

🔗 [Documentación completa](http://localhost:8000/api/docs/)

---

## 🧪 Ejecutar tests

Para ejecutar todos los tests:

```bash
docker-compose exec web pytest
```

La suite de tests incluye cobertura de:

- Autenticación (registro, login, cambio de contraseña)
- Usuarios (actualización de perfil, eliminación)
- Ingresos (Income)
- Gastos (Expense)
- Metas de ahorro (SavingGoal)
- Categorías (Category)
- Notificaciones (Notification)
- Reflexiones personales (Reflection)
- Planes mensuales Kakeibo (MonthlyPlan)
- Categorización con IA (modelo, reentrenamiento y validación)
- Criptomonedas (Cripto)
- Panel administrativo (estadísticas y modelo de IA)

Además, puedes generar un informe de cobertura con:

```bash
docker-compose exec web pytest --cov=savings --cov-report=term-missing
```

---

## 🌐 WebSocket en tiempo real

Zenkoo permite recibir actualizaciones de precios de criptomonedas (BTC, ETH, USDT) en tiempo real mediante **WebSocket**, sin necesidad de recargar la página.

### 🔌 URL del WebSocket
- Local (desarrollo):
```bash
ws://localhost:8000/ws/criptos/
```

- Producción (si usas HTTPS):
```bash
wss://tudominio.com/ws/criptos/
```

### 🧪 Ejemplo de conexión desde el cliente

```ts
const socket = new WebSocket('ws://localhost:8000/ws/criptos/');

socket.onopen = () => {
console.log('🟢 Conectado al WebSocket de criptos');
};

socket.onmessage = (event) => {
const data = JSON.parse(event.data);
console.log('📈 Precio actualizado:', data);
};

socket.onclose = () => {
console.log('🔴 Conexión cerrada');
};
```
### 🔔 ¿Qué datos se envían?

Cada vez que se actualiza el precio de una criptomoneda:

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

```md
| Campo      | Descripción                        |
|------------|------------------------------------|
| `type`     | Tipo de mensaje (`update_price`)   |
| `symbol`   | Criptomoneda (`BTC`, `ETH`, `USDT`)|
| `price`    | Precio actualizado                 |
| `timestamp`| Fecha y hora de la actualización   |

---

## 🤖 Categorización automática con IA

Zenkoo incluye una IA básica que clasifica automáticamente los gastos e ingresos según el método Kakeibo. Utiliza:

- **scikit-learn** con `TfidfVectorizer` + `Naive Bayes`
- Entrenamiento desde base de datos real
- Archivo `model.pkl` almacenado en `static/ml/`
- Endpoint de administración:
  - GET `/api/admin/model-info/` → Info del modelo actual
  - POST `/api/admin/retrain/` → Reentrena el modelo desde BD

Solo accesible para usuarios administradores (`is_staff=True`).

---

## 📌 Endpoints principales

```bash
| Recurso          | Método   | Ruta                       | Descripción                           |
|------------------|----------|----------------------------|---------------------------------------|
| Usuarios         | POST     | /api/users/register/       | Registro                              |
|                  | POST     | /api/users/login/          | Login (JWT)                           |
| Ingresos         | GET/POST | /api/incomes/              | Listado y creación de ingresos        |
| Gastos           | GET/POST | /api/expenses/             | Listado y creación de gastos          |
| Metas de ahorro  | GET/POST | /api/saving-goals/         | Listado y creación de metas           |
| Categorías       | GET/POST | /api/categories/           | Listado y creación de categorías      |
| Reflexiones      | GET/POST | /api/reflections/          | Reflexiones mensuales                 |
| Plan mensual     | GET      | /api/monthly-plan/current/ | Resumen mensual (Kakeibo)             |
|                  | POST     | /api/monthly-plan/         | Crear o editar plan mensual           |
| Criptomonedas    | GET      | /api/criptos/              | Últimos precios (BTC, ETH, USDT, etc.)|
```

---

## 📂 Estructura del proyecto

```bash
zenkoo-backend/
│
├── backend/                      # Configuración principal del proyecto Django
│   ├── asgi.py                   # Configuración ASGI (para WebSockets con Daphne)
│   ├── wsgi.py                   # Configuración WSGI (para Gunicorn)
│   ├── routing.py                # Rutas de WebSocket (canales de Django Channels)
│   ├── settings.py               # Configuración global del proyecto (base de datos, apps, etc.)
│   ├── urls.py                   # Rutas principales de la API
│   └── __init__.py               # Archivo para marcar como módulo Python
│
├── savings/                      # App principal: lógica del negocio y API REST
│   ├── admin.py                  # Configuración del panel de administración
│   ├── apps.py                   # Configuración de la app 'savings'
│   ├── consumers/                # WebSockets para criptos y notificaciones
│   ├── filters/                  # Filtros personalizados para listados
│   ├── management/               # Comandos custom de Django (crear superusuario, etc.)
│   ├── migrations/               # Migraciones de la base de datos
│   ├── ml/                       # IA: modelo de categorización, entrenamiento y predicción
│   ├── models/                   # Modelos desacoplados (Expense, Income, User, etc.)
│   ├── scripts/                  # Scripts adicionales como integración cron
│   ├── static/                   # Archivos estáticos (modelo IA, JSON, etc.)
│   ├── tests/                    # Suite de tests completa con `pytest`
│   ├── views/                    # Vistas organizadas por dominio (gastos, IA, admin, etc.)
│   ├── serializers.py            # Serializadores DRF (IncomeSerializer, etc.)
│   ├── urls.py                   # Rutas internas de la app
│   ├── pagination.py             # Paginación personalizada
│   └── views.py                  # Entrada por defecto (puede no usarse si se modulariza)
│
├── staticfiles/                  # Archivos estáticos recolectados (admin, Swagger, modelo IA)
│   ├── ml/                       # Modelo entrenado (model.pkl) y metadatos (model_info.json)
│   └── ...                       # Otros recursos de admin y DRF
│
├── docker-compose.yml            # Orquestación de servicios: web, db, nginx
├── Dockerfile                    # Imagen del backend (Python + Uvicorn + Gunicorn + Daphne)
├── entrypoint.sh                 # Script de arranque para el contenedor web
├── cron_update_criptos.py        # Script ejecutado por cron para actualizar precios cripto
├── crontabfile                   # Entradas cron configuradas al build
├── cron_criptos.log              # Log del cron (preconfigurado para pruebas)
├── db.sqlite3                    # Base de datos por defecto (solo para pruebas locales)
├── manage.py                     # CLI para interactuar con el proyecto Django
├── pytest.ini                    # Configuración de pytest (paths, flags, etc.)
├── requirements.txt              # Dependencias del backend en Python
├── Zenkoo API.yaml               # Esquema OpenAPI generado con `drf-spectacular`
└── README.md                     # Documentación del proyecto
```

---

## 🧑‍💻 Autor

Desarrollado por [Albert Clemente](https://github.com/AlbertClemente) como proyecto final del Ciclo Formativo de Grado Superior de Desarrollo de Aplicaciones Web en [Ilerna](https://www.ilerna.es/).  
Proyecto educativo sin ánimo de lucro.

---

```md
> 🇪🇸 Este README está en español. [Switch to English](README.en.md) (coming soon).
