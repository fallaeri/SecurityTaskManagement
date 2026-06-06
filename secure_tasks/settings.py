"""
secure_tasks/settings.py
Secure configuration for Secure Task Management System
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ─── CORE ────────────────────────────────────────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# ─── APPS ────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Security
    "axes",
    # Project apps
    "auth_app",
    "task_app",
    "user_app",
    "audit_app",
    "upload_app",
]

# ─── MIDDLEWARE ───────────────────────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "axes.middleware.AxesMiddleware",                        # login lockout
    "audit_app.middleware.AuditMiddleware",                  # our audit logger
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "secure_tasks.urls"

# ─── TEMPLATES ───────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "autoescape": True,   # XSS protection: always on
        },
    },
]

WSGI_APPLICATION = "secure_tasks.wsgi.application"

# ─── DATABASE ────────────────────────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ─── PASSWORD SECURITY ───────────────────────────────────────────────────────
# Argon2 is memory-hard and GPU-resistant (better than PBKDF2)
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",   # fallback
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 12}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─── SESSION SECURITY ────────────────────────────────────────────────────────
SESSION_COOKIE_HTTPONLY = True        # JS cannot read session cookie
SESSION_COOKIE_SECURE = not DEBUG     # HTTPS only in production
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_AGE = int(os.getenv("SESSION_COOKIE_AGE", 1800))  # 30 min
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# ─── CSRF SECURITY ───────────────────────────────────────────────────────────
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SAMESITE = "Lax"

# ─── SECURITY HEADERS ────────────────────────────────────────────────────────
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# ─── DJANGO-AXES (Login Brute Force Protection) ───────────────────────────────
AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]
AXES_FAILURE_LIMIT = 5          # lock after 5 failed attempts
AXES_COOLOFF_TIME = 0.5         # 30 minutes lockout
AXES_LOCKOUT_TEMPLATE = "errors/lockout.html"
AXES_RESET_ON_SUCCESS = True

# ─── FILE UPLOADS ────────────────────────────────────────────────────────────
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024   # 5 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024
ALLOWED_UPLOAD_EXTENSIONS = [".pdf", ".png", ".jpg", ".jpeg"]
ALLOWED_UPLOAD_MIME_TYPES = ["application/pdf", "image/png", "image/jpeg"]

# ─── STATIC FILES ────────────────────────────────────────────────────────────
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# ─── AUTH REDIRECTS ──────────────────────────────────────────────────────────
LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "/tasks/"
LOGOUT_REDIRECT_URL = "/auth/login/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
