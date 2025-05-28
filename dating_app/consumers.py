
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

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.match_id = self.scope['url_route']['kwargs']['match_id']
        self.room_group_name = f'chat_{self.match_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']
        sender_username = text_data_json['sender']

        # Save message to database
        message = await self.save_message(message_content, sender_username)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    'id': message.id,
                    'content': message.content,
                    'sender': message.sender.username,
                    'created_at': message.created_at.isoformat()
                }
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def save_message(self, content, sender_username):
        user = User.objects.get(username=sender_username)
        match = Match.objects.get(id=self.match_id)
        return Message.objects.create(
            match=match,
            sender=user,
            content=content
        )
