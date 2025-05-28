
import json
import os
import django
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dating_app.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Match, Message

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
            return
        
        self.user_id = self.scope["user"].id
        self.notification_group_name = f'notifications_{self.user_id}'

        # Join notification group
        await self.channel_layer.group_add(
            self.notification_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave notification group
        if hasattr(self, 'notification_group_name'):
            await self.channel_layer.group_discard(
                self.notification_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        # Handle incoming WebSocket messages if needed
        pass

    async def match_notification(self, event):
        # Send match notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'match',
            'message': event['message'],
            'other_user': event['other_user']
        }))

    async def message_notification(self, event):
        # Send message notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'sender': event['sender'],
            'match_id': event['match_id']
        }))
