import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CriptoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'message': 'Conexión WebSocket establecida con éxito'
        }))

    async def disconnect(self, close_code):
        print("WebSocket desconectado")

    async def receive(self, text_data):
        data = json.loads(text_data)
        print("Mensaje recibido:", data)