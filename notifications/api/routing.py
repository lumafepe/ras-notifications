# your_app/routing.py

from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r'ws/notifications/<user_id>', consumers.NotificationConsumer.as_asgi()),
]
