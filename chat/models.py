from django.db import models
from users.models import AuraUser

class DirectChat(models.Model):
    users = models.ManyToManyField(AuraUser)
    created = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    chat = models.ForeignKey(DirectChat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(AuraUser, on_delete=models.CASCADE)

    ciphertext = models.TextField()
    encrypted_key = models.TextField()
    iv = models.CharField(max_length=64)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["created"]),
        ]
