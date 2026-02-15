import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()
            return
        self.user = user
        await self.channel_layer.group_add("status", self.channel_name)
        await self.accept()
        await self.update_status("online")

    async def disconnect(self, close_code):
        await self.update_status("offline")
        await self.channel_layer.group_discard("status", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data["type"] == "status":
            await self.update_status(data["status"])

    async def update_status(self, status):
        await database_sync_to_async(self._update_status)(status)
        await self.channel_layer.group_send(
            "status",
            {
                "type": "broadcast_status",
                "user": self.user.aura_id,
                "status": status,
            }
        )

    def _update_status(self, status):
        self.user.status = status
        self.user.last_seen = timezone.now()
        self.user.save()

    async def broadcast_status(self, event):
        await self.send(text_data=json.dumps(event))
