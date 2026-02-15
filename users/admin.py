from django.contrib import admin
from .models import AuraUser, FriendRequest, Friend
from django.contrib.auth.admin import UserAdmin

@admin.register(AuraUser)
class AuraUserAdmin(UserAdmin):
    model = AuraUser
    list_display = ("username", "email", "aura_id", "status", "last_seen")

admin.site.register(FriendRequest)
admin.site.register(Friend)
