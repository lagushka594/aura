from django.urls import re_path
from users.consumers import StatusConsumer
from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/status/$", StatusConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<chat_id>\d+)/$", ChatConsumer.as_asgi()),
]
