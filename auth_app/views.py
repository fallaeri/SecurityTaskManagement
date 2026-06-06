"""auth_app/views.py"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_ratelimit.decorators import ratelimit

from .forms import RegisterForm, LoginForm
from user_app.models import UserProfile
from audit_app.utils import log_action


@ratelimit(key="ip", rate="10/m", method="POST", block=True)
def register_view(request):
    if request.user.is_authenticated:
        return redirect("task_list")

    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        # Create default UserProfile with role=user
        UserProfile.objects.create(user=user, role="user")
        log_action(request, "LOGIN", f"New user registered: {user.username}")
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        messages.success(request, "Welcome! Your account has been created.")
        return redirect("task_list")

    return render(request, "auth_app/register.html", {"form": form})


@ratelimit(key="ip", rate="10/m", method="POST", block=True)
def login_view(request):
    if request.user.is_authenticated:
        return redirect("task_list")

    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            log_action(request, "LOGIN", f"User logged in: {user.username}")
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect("task_list")
        else:
            log_action(request, "LOGIN_FAILED",
                       f"Failed login for: {request.POST.get('username', '')}")
            messages.error(request, "Invalid username or password.")

    return render(request, "auth_app/login.html", {"form": form})


@login_required
def logout_view(request):
    if request.method == "POST":
        log_action(request, "LOGOUT", f"User logged out: {request.user.username}")
        logout(request)
        messages.info(request, "You have been logged out.")
    return redirect("login")


# ─── Custom error handlers ────────────────────────────────────────────────────
def error_403(request, exception=None):
    return render(request, "errors/403.html", status=403)


def error_404(request, exception=None):
    return render(request, "errors/404.html", status=404)
