from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random

def generate_code():
    return str(random.randint(1000, 9999))

class AuraUser(AbstractUser):
    email = models.EmailField(unique=True)
    unique_code = models.CharField(max_length=4, editable=False)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    STATUS_CHOICES = [
        ("online", "Online"),
        ("idle", "Idle"),
        ("offline", "Offline"),
        ("invisible", "Invisible"),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="offline")
    last_seen = models.DateTimeField(default=timezone.now)

    REQUIRED_FIELDS = ["email"]

    def save(self, *args, **kwargs):
        if not self.unique_code:
            code = generate_code()
            while AuraUser.objects.filter(username=self.username, unique_code=code).exists():
                code = generate_code()
            self.unique_code = code
        super().save(*args, **kwargs)

    @property
    def aura_id(self):
        return f"{self.username}#{self.unique_code}"

class FriendRequest(models.Model):
    from_user = models.ForeignKey(AuraUser, related_name="sent_requests", on_delete=models.CASCADE)
    to_user = models.ForeignKey(AuraUser, related_name="received_requests", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

class Friend(models.Model):
    user = models.ForeignKey(AuraUser, related_name="friends", on_delete=models.CASCADE)
    friend = models.ForeignKey(AuraUser, related_name="related_to", on_delete=models.CASCADE)
