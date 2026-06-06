"""user_app/urls.py"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.profile_view, name="profile"),
]
