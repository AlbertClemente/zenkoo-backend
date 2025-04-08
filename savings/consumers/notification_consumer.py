import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f"user_{self.user_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

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

        # Enviar mensaje a todos en el grupo usando `send_notification`
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "send_notification",
                "message": data.get("message"),
            }
        )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            "type": "new_notification",  # Para el hook en el front!
            "message": event["message"]
        }))