"""audit_app/utils.py — helper used by views to log actions"""
from .models import AuditLog


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def log_action(request, action, detail=""):
    """Call this from any view: log_action(request, 'TASK_CREATE', 'Task: Fix bug')"""
    AuditLog.objects.create(
        user=request.user if request.user.is_authenticated else None,
        action=action,
        detail=detail[:500],
        ip_address=get_client_ip(request),
    )
