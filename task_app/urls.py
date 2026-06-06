"""task_app/urls.py"""
from django.urls import path
from . import views

urlpatterns = [
    path("",              views.task_list,   name="task_list"),
    path("create/",       views.task_create, name="task_create"),
    path("<uuid:pk>/",    views.task_detail, name="task_detail"),
    path("<uuid:pk>/edit/",   views.task_update, name="task_update"),
    path("<uuid:pk>/delete/", views.task_delete, name="task_delete"),
]
