import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables desde .env si existen
load_dotenv()

# Permitir override por variable de entorno (útil al usar docker-compose exec -e ...)
LOGIN_URL = os.getenv("LOGIN_URL", "http://web:8000/api/users/login/")
UPDATE_URL = os.getenv("UPDATE_URL", "http://web:8000/api/criptos/update/")

email = os.getenv("ZENKOO_CRON_EMAIL")
password = os.getenv("ZENKOO_CRON_PASSWORD")

timestamp = datetime.now().isoformat()

if not email or not password:
    print(f"{timestamp} [ERROR] Faltan las variables ZENKOO_CRON_EMAIL o ZENKOO_CRON_PASSWORD")
    exit(1)

# Obtener token
credentials = {"email": email, "password": password}
print(f"{timestamp} [INFO] Haciendo login con {email} en {LOGIN_URL}")
token_response = requests.post(LOGIN_URL, json=credentials)

if token_response.status_code != 200:
    print(f"{timestamp} [ERROR] No se pudo obtener token: {token_response.text}")
    exit(1)

access_token = token_response.json().get("access")
headers = {"Authorization": f"Bearer {access_token}"}

# POST a /criptos/update/
response = requests.post(UPDATE_URL, headers=headers)

if response.status_code == 200:
    print(f"{timestamp} [OK] Criptos actualizadas correctamente")
    criptos = response.json()
    for cripto in criptos:
        name = cripto.get("name")
        symbol = cripto.get("symbol")
        price = cripto.get("price")
        cripto_time = cripto.get("timestamp")
        print(f"{timestamp} [INFO] {name} ({symbol}): {price} EUR - actualizado en {cripto_time}")
else:
    print(f"{timestamp} [ERROR] Código {response.status_code}: {response.text}")
