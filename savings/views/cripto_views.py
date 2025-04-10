import requests
from decimal import Decimal, InvalidOperation, ROUND_DOWN
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from savings.models import User, Cripto, Notification
from savings.serializers import CriptoSerializer
from django.utils.timezone import now, timedelta
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Documentación
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

@extend_schema(
    tags=["Criptos"],
    summary="Listar criptomonedas",
    responses={
        200: CriptoSerializer(many=True),
        401: OpenApiResponse(description="No autenticado")
    },
)
class CriptoListView(ListAPIView):
    serializer_class = CriptoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cripto.objects.all().order_by('name')

@extend_schema(
    tags=["Criptos"],
    summary="Actualizar precios desde CoinGecko",
    responses={
        200: CriptoSerializer(many=True),
        401: OpenApiResponse(description="No autenticado"),
        500: OpenApiResponse(description="Error al conectar con CoinGecko")
    },
)
class CriptoUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CriptoSerializer

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

            # Buscar cripto antes
            old_cripto = Cripto.objects.filter(symbol=datos['symbol']).first()
            old_price = old_cripto.price if old_cripto else None

            # Actualizar o crear
            cripto, created = Cripto.objects.update_or_create(
                symbol=datos['symbol'],
                defaults={
                    'name': nombre,
                    'price': price_decimal,
                    'timestamp': now()
                }
            )

            # Si el precio ha variado a partir de un 1% o se ha creado nueva cripto
            if created or (
                    old_price is not None and abs((price_decimal - old_price) / old_price) >= Decimal("0.01")
            ):
                # Comprobar antes que nada que Channels está bien configurado
                channel_layer = get_channel_layer()
                if channel_layer is None:
                    print("[ERROR] channel_layer es None, ¿Channels está bien configurado?")
                    return Response({'[ERROR]': 'No se pudo enviar notificación WebSocket'}, status=500)

                # Enviaremos notificación a todos los usuarios suscritos, menos al del cron
                usuarios_destino = User.objects.exclude(email="cronjob@zenkoo.com")

                for user in usuarios_destino:
                    # Evitamos notificar el mismo precio
                    ya_notificado = Notification.objects.filter(
                        user=user,
                        type="cripto",
                        message__icontains=cripto.name,
                        created_at__gte=now() - timedelta(hours=1)
                    ).exists()

                    if ya_notificado:
                        print(f"[SKIP] Ya se notificó {cripto.name} a {user.email} en la última hora.")
                        continue

                    # Crear la notificación para ese user
                    notification = Notification.objects.create(
                        user=user,
                        message=f"{cripto.name} está en {cripto.price}€ 🎉",
                        type="cripto"
                    )

                    # Emitir la notificación por WebSocket
                    print(f"[WS DEBUG] Enviando notificación a grupo user_{str(user.id)}")
                    async_to_sync(channel_layer.group_send)(
                        f"user_{str(user.id)}",
                        {
                            "type": "send_notification",
                            "data": {
                                "id": str(notification.id),
                                "message": notification.message,
                                "is_read": notification.is_read,
                                "created_at": notification.created_at.isoformat(),
                                "user": str(notification.user_id),
                                "type": notification.type
                            }
                        }
                    )

            resultados.append(CriptoSerializer(cripto).data)

        return Response(resultados)
