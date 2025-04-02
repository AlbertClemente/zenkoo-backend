from django.urls import path
from savings.consumers.cripto_consumer import CriptoPriceConsumer

websocket_urlpatterns = [
    path("ws/criptos/", CriptoPriceConsumer.as_asgi()),
]