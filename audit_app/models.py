"""audit_app/models.py — AuditLog model"""
import uuid
from django.db import models
from django.contrib.auth.models import User


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ("LOGIN",          "Login"),
        ("LOGOUT",         "Logout"),
        ("LOGIN_FAILED",   "Login Failed"),
        ("TASK_CREATE",    "Task Created"),
        ("TASK_UPDATE",    "Task Updated"),
        ("TASK_DELETE",    "Task Deleted"),
        ("FILE_UPLOAD",    "File Uploaded"),
        ("PROFILE_UPDATE", "Profile Updated"),
    ]

    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action     = models.CharField(max_length=30, choices=ACTION_CHOICES)
    detail     = models.CharField(max_length=500, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.timestamp:%Y-%m-%d %H:%M} | {self.action} | {self.user}"
