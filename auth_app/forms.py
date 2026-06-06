"""auth_app/forms.py"""
import bleach
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "12+ characters"}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Repeat password"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        widgets = {
            "username":   forms.TextInput(attrs={"class": "form-control"}),
            "email":      forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name":  forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_username(self):
        username = bleach.clean(self.cleaned_data["username"].strip())
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get("password1", "")
        if len(password) < 12:
            raise ValidationError("Password must be at least 12 characters.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "autofocus": True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
