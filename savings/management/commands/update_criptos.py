import requests
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from savings.models import Cripto

class Command(BaseCommand):
    help = 'Actualiza los precios de las criptomonedas desde CoinGecko'

    def handle(self, *args, **kwargs):
        url = 'https://api.coingecko.com/api/v3/simple/price'
        params = {
            'ids': 'bitcoin,ethereum,tether',
            'vs_currencies': 'eur'
        }
        response = requests.get(url, params=params)

        if response.status_code != 200:
            self.stderr.write('¡Error al conectar con CoinGecko!')
            return

        data = response.json()

        for nombre, datos in {
            'Bitcoin': {'symbol': 'BTC', 'price': data.get('bitcoin', {}).get('eur')},
            'Ethereum': {'symbol': 'ETH', 'price': data.get('ethereum', {}).get('eur')},
            'Tether': {'symbol': 'USDT', 'price': data.get('tether', {}).get('eur')}
        }.items():
            price = datos['price']
            if price is None:
                continue

            try:
                price_decimal = Decimal(str(price))
            except (InvalidOperation, TypeError, ValueError) as e:
                self.stderr.write(f"[ERROR] Decimal conversion failed: {price} -> {e}")
                continue

            cripto, _ = Cripto.objects.update_or_create(
                symbol=datos['symbol'],
                defaults={
                    'name': nombre,
                    'price': price_decimal,
                    'timestamp': now()
                }
            )
            self.stdout.write(f"{cripto.name} actualizado a {cripto.price} EUR")