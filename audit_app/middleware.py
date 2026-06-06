"""audit_app/middleware.py — Automatic audit logging middleware"""
from .models import AuditLog


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


class AuditMiddleware:
    """Logs login and logout events automatically."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        was_authenticated = request.user.is_authenticated
        response = self.get_response(request)

        # Detect logout (was logged in, now anonymous, POST to logout URL)
        if was_authenticated and not request.user.is_authenticated:
            AuditLog.objects.create(
                user=None,
                action="LOGOUT",
                detail="Session ended",
                ip_address=get_client_ip(request),
            )
        return response
