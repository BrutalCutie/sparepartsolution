from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from users.models import User


class UserRegistrationsForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "name",
            "phone",
            "email",
            "password1",
            "password2",
        )


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "name",
            "phone",
            "image",
        )
