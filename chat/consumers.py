import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, DirectChat
from users.models import AuraUser

PAGE_SIZE = 20

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room = f"chat_{self.chat_id}"
        await self.channel_layer.group_add(self.room, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data["type"] == "message":
            msg = await self.save_message(data)
            await self.channel_layer.group_send(
                self.room,
                {
                    "type": "chat_message",
                    "message": msg,
                }
            )

        if data["type"] == "history":
            messages = await self.get_history(data.get("page", 1))
            await self.send(text_data=json.dumps({
                "type": "history",
                "messages": messages
            }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "message",
            "message": event["message"]
        }))

    @database_sync_to_async
    def save_message(self, data):
        chat = DirectChat.objects.get(id=self.chat_id)
        sender = AuraUser.objects.get(id=data["sender"])
        msg = Message.objects.create(
            chat=chat,
            sender=sender,
            ciphertext=data["ciphertext"],
            encrypted_key=data["encrypted_key"],
            iv=data["iv"]
        )
        return {
            "sender": sender.aura_id,
            "ciphertext": msg.ciphertext,
            "encrypted_key": msg.encrypted_key,
            "iv": msg.iv,
            "created": msg.created.isoformat()
        }

    @database_sync_to_async
    def get_history(self, page):
        offset = (page - 1) * PAGE_SIZE
        qs = Message.objects.filter(chat_id=self.chat_id)[offset:offset + PAGE_SIZE]
        return [{
            "sender": m.sender.aura_id,
            "ciphertext": m.ciphertext,
            "encrypted_key": m.encrypted_key,
            "iv": m.iv,
            "created": m.created.isoformat()
        } for m in qs]
