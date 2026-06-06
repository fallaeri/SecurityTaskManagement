"""task_app/models.py — Task model"""
import uuid
from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    PRIORITY_CHOICES = [("low", "Low"), ("medium", "Medium"), ("high", "High")]
    STATUS_CHOICES   = [("todo", "To Do"), ("in_progress", "In Progress"), ("done", "Done")]

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner       = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True, max_length=2000)
    priority    = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    status      = models.CharField(max_length=15, choices=STATUS_CHOICES, default="todo")
    due_date    = models.DateField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
