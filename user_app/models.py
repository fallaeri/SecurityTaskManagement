"""user_app/models.py — UserProfile model"""
import uuid
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [("admin", "Admin"), ("user", "User")]

    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role       = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    bio        = models.TextField(blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_admin(self):
        return self.role == "admin"

    def __str__(self):
        return f"{self.user.username} ({self.role})"
