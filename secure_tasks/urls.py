"""secure_tasks/urls.py"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/",    admin.site.urls),
    path("auth/",     include("auth_app.urls")),
    path("tasks/",    include("task_app.urls")),
    path("profile/",  include("user_app.urls")),
    path("audit/",    include("audit_app.urls")),
    path("uploads/",  include("upload_app.urls")),
    path("",          include("task_app.urls")),   # root → dashboard
]

# Serve media in dev
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error pages
handler403 = "auth_app.views.error_403"
handler404 = "auth_app.views.error_404"
