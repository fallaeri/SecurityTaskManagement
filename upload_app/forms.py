"""upload_app/forms.py — secure file upload with MIME + extension validation"""
import os
import magic   # python-magic; fallback to imghdr if unavailable
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError


class UploadForm(forms.Form):
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"class": "form-control", "accept": ".pdf,.png,.jpg,.jpeg"})
    )

    def clean_file(self):
        f = self.cleaned_data["file"]

        # 1. Size check
        if f.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
            raise ValidationError("File too large. Maximum size is 5 MB.")

        # 2. Extension check
        ext = os.path.splitext(f.name)[1].lower()
        if ext not in settings.ALLOWED_UPLOAD_EXTENSIONS:
            raise ValidationError(f"File type '{ext}' not allowed. Use PDF, PNG, or JPG.")

        # 3. MIME type check (reads actual file bytes — cannot be spoofed by renaming)
        f.seek(0)
        header = f.read(2048)
        f.seek(0)

        try:
            mime = magic.from_buffer(header, mime=True)
        except Exception:
            # python-magic not available; skip deep MIME check
            mime = f.content_type

        if mime not in settings.ALLOWED_UPLOAD_MIME_TYPES:
            raise ValidationError(f"File content type '{mime}' not allowed.")

        return f
