import json
from channels.generic.websocket import AsyncWebsocketConsumer
from savings.models import Cripto
from asgiref.sync import sync_to_async

class CriptoPriceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("cripto_prices", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("cripto_prices", self.channel_name)

    async def receive(self, text_data):
        # Este consumer no espera mensajes entrantes del cliente.
        pass

    async def send_cripto_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))