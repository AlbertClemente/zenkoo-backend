import json
from channels.generic.websocket import AsyncWebsocketConsumer
from savings.models import Notification
from asgiref.sync import sync_to_async
from uuid import UUID

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f"user_{self.user_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        print(f"[WS CONNECT] Me uno al grupo: {self.group_name}")

        await self.accept()
        print(f"WebSocket conectado para {self.group_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(f"Mensaje recibido en {self.group_name}: {text_data}")

        data = json.loads(text_data)
        message = data.get("message")
        notification_type = data.get("type", "general")

        # Guardar en la base de datos
        notification = await sync_to_async(Notification.objects.create)(
            user_id=UUID(self.user_id),
            message=message,
            is_read=False,
            type=notification_type
        )

        # Serializar
        notification_data = {
            "id": str(notification.id),
            "message": notification.message,
            "is_read": notification.is_read,
            "created_at": notification.created_at.isoformat(),
            "user": str(notification.user_id),
            "type": notification_type
        }


        print(f"[ACDEBUG] notification data: {notification_data}")
        # Enviar mensaje a todos en el grupo usando `send_notification`
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "send_notification",
                "data": notification_data  # nota: pasa todo como `data`
            }
        )

    async def send_notification(self, event):
        print(f"[WS SEND] Enviando a {self.group_name}: {event['data']['message']}")
        await self.send(text_data=json.dumps(event["data"]))