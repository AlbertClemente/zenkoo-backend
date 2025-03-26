from django.urls import path
from savings.consumers import CriptoConsumer

websocket_urlpatterns = [
    path('ws/cripto/', CriptoConsumer.as_asgi()),
]