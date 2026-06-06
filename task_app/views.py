"""task_app/views.py — CRUD with RBAC + IDOR prevention"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from .models import Task
from .forms import TaskForm
from audit_app.utils import log_action


def _get_task_for_user(task_id, user):
    """
    Fetch a task safely.
    - Admin can access any task.
    - Regular user can only access their own task (prevents IDOR).
    """
    task = get_object_or_404(Task, pk=task_id)
    profile = getattr(user, "profile", None)
    if profile and profile.is_admin():
        return task
    if task.owner != user:
        raise PermissionDenied   # returns HTTP 403
    return task


@login_required
def task_list(request):
    profile = getattr(request.user, "profile", None)
    if profile and profile.is_admin():
        tasks = Task.objects.select_related("owner").all()
    else:
        tasks = Task.objects.filter(owner=request.user)

    return render(request, "task_app/task_list.html", {
        "tasks": tasks,
        "is_admin": profile and profile.is_admin(),
    })


@login_required
def task_create(request):
    form = TaskForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        task = form.save(commit=False)
        task.owner = request.user
        task.save()
        log_action(request, "TASK_CREATE", f"Task created: {task.title}")
        messages.success(request, "Task created successfully.")
        return redirect("task_list")

    return render(request, "task_app/task_form.html", {"form": form, "action": "Create"})


@login_required
def task_detail(request, pk):
    task = _get_task_for_user(pk, request.user)
    return render(request, "task_app/task_detail.html", {"task": task})


@login_required
def task_update(request, pk):
    task = _get_task_for_user(pk, request.user)
    form = TaskForm(request.POST or None, instance=task)
    if request.method == "POST" and form.is_valid():
        form.save()
        log_action(request, "TASK_UPDATE", f"Task updated: {task.title}")
        messages.success(request, "Task updated.")
        return redirect("task_list")

    return render(request, "task_app/task_form.html", {"form": form, "action": "Update", "task": task})


@login_required
def task_delete(request, pk):
    task = _get_task_for_user(pk, request.user)
    if request.method == "POST":
        title = task.title
        task.delete()
        log_action(request, "TASK_DELETE", f"Task deleted: {title}")
        messages.warning(request, f'Task "{title}" deleted.')
        return redirect("task_list")

    return render(request, "task_app/task_confirm_delete.html", {"task": task})
