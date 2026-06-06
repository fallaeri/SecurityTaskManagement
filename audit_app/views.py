"""audit_app/views.py — admin-only log viewer"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from .models import AuditLog


@login_required
def audit_log_view(request):
    profile = getattr(request.user, "profile", None)
    if not profile or not profile.is_admin():
        raise PermissionDenied   # non-admins get 403

    logs = AuditLog.objects.select_related("user").all()
    paginator = Paginator(logs, 25)
    page = paginator.get_page(request.GET.get("page"))

    return render(request, "audit_app/audit_log.html", {"page_obj": page})
