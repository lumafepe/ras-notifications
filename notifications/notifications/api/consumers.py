# your_app/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = self.scope['url_route']['kwargs']['user_id']
        await self.channel_layer.group_add(f'user_{user_id}', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        user_id = self.scope['url_route']['kwargs']['user_id']
        await self.channel_layer.group_discard(f'user_{user_id}', self.channel_name)

    async def send_notification(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))
