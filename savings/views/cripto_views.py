import requests
from decimal import Decimal, InvalidOperation, ROUND_DOWN
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from savings.models import Cripto
from savings.serializers import CriptoSerializer
from django.utils.timezone import now
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class CriptoListView(ListAPIView):
    serializer_class = CriptoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cripto.objects.all().order_by('name')

class CriptoUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        url = 'https://api.coingecko.com/api/v3/simple/price'
        params = {
            'ids': 'bitcoin,ethereum,tether',
            'vs_currencies': 'eur'
        }
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return Response({'error': 'Error al conectar con CoinGecko'}, status=500)

        data = response.json()

        resultados = []
        for nombre, datos in {
            'Bitcoin': {'symbol': 'BTC', 'price': data.get('bitcoin', {}).get('eur')},
            'Ethereum': {'symbol': 'ETH', 'price': data.get('ethereum', {}).get('eur')},
            'Tether': {'symbol': 'USDT', 'price': data.get('tether', {}).get('eur')}
        }.items():
            price = datos['price']
            print(f"[DEBUG] Cripto: {nombre}, Precio bruto: {price} ({type(price)})")
            if price is None:
                continue

            try:
                price_decimal = Decimal(str(price))
            except (InvalidOperation, TypeError, ValueError) as e:
                print(f"[ERROR] Conversión Decimal fallida: {price} -> {e}")
                continue

            cripto, _ = Cripto.objects.update_or_create(
                symbol=datos['symbol'],
                defaults={
                    'name': nombre,
                    'price': price_decimal,
                    'timestamp': now()
                }
            )

            # Emitimos por WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "cripto_prices",
                {
                    "type": "send_cripto_update",
                    "data": {
                        "name": cripto.name,
                        "symbol": cripto.symbol,
                        "price": str(cripto.price),
                        "timestamp": str(cripto.timestamp),
                    },
                }
            )

            resultados.append(CriptoSerializer(cripto).data)

        return Response(resultados)
