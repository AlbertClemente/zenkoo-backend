from django.urls import re_path
from savings.consumers.cripto_consumer import CriptoPriceConsumer

websocket_urlpatterns = [
    re_path(r'ws/criptos/$', CriptoPriceConsumer.as_asgi()),
]