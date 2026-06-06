"""secure_tasks/wsgi.py"""
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "secure_tasks.settings")
application = get_wsgi_application()
