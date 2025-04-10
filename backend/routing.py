from django.urls import re_path
from savings.consumers.cripto_consumer import CriptoPriceConsumer
from savings.consumers.notification_consumer import NotificationConsumer

websocket_urlpatterns = [
    re_path(r'ws/criptos/$', CriptoPriceConsumer.as_asgi()),
    re_path(r'ws/notifications/(?P<user_id>[0-9a-f-]+)/$', NotificationConsumer.as_asgi()),
]