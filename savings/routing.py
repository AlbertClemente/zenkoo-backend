from django.urls import path, re_path
from savings.consumers.cripto_consumer import CriptoPriceConsumer
from savings.consumers.notification_consumer import NotificationConsumer

websocket_urlpatterns = [
    path("ws/criptos/", CriptoPriceConsumer.as_asgi()),
    re_path(r"ws/notifications/(?P<user_id>[^/]+)/$", NotificationConsumer.as_asgi()),
]