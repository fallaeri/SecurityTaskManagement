"""task_app/forms.py"""
import bleach
from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "priority", "status", "due_date"]
        widgets = {
            "title":       forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "priority":    forms.Select(attrs={"class": "form-select"}),
            "status":      forms.Select(attrs={"class": "form-select"}),
            "due_date":    forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def clean_title(self):
        """Sanitise title to strip any injected HTML."""
        return bleach.clean(self.cleaned_data["title"].strip(), tags=[], strip=True)

    def clean_description(self):
        """Allow only safe tags in description."""
        allowed = ["b", "i", "u", "em", "strong", "p", "br", "ul", "li"]
        return bleach.clean(self.cleaned_data["description"], tags=allowed, strip=True)
