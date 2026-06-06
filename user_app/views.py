"""user_app/views.py"""
import bleach
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import UserProfile
from audit_app.utils import log_action


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30, required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        max_length=30, required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = UserProfile
        fields = ["bio"]
        widgets = {
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3, "maxlength": 500}),
        }

    def clean_bio(self):
        return bleach.clean(self.cleaned_data["bio"], tags=[], strip=True)


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user, defaults={"role": "user"})

    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # Update User fields
            request.user.first_name = bleach.clean(form.cleaned_data["first_name"], tags=[], strip=True)
            request.user.last_name  = bleach.clean(form.cleaned_data["last_name"],  tags=[], strip=True)
            request.user.save()
            form.save()
            log_action(request, "PROFILE_UPDATE", "Profile updated")
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")

    return render(request, "user_app/profile.html", {
        "profile": profile,
        "form": form,
    })
