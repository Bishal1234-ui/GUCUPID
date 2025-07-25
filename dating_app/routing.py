
from django.urls import re_path
from . import consumers
from .notifications_consumer import NotificationConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<match_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
]
