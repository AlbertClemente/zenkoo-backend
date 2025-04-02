from django.urls import re_path
from savings.consumers import Crip

websocket_urlpatterns = [
    re_path(r'ws/criptos/$', CriptoConsumer.as_asgi()),
]