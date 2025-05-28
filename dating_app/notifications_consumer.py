
import json
import os
import django
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dating_app.settings')
django.setup()

from django.contrib.auth.models import User

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.user_group_name = f'user_{self.user.id}'
            
            # Join user-specific group
            await self.channel_layer.group_add(
                self.user_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'user_group_name'):
            await self.channel_layer.group_discard(
                self.user_group_name,
                self.channel_name
            )

    # Receive message from room group
    async def send_notification(self, event):
        notification = event['notification']
        
        # Send notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': notification['type'],
            'message': notification['message'],
            'data': notification.get('data', {})
        }))
