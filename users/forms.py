from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from users.models import User


class UserRegistrationsForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "name",
            "phone",
            "email",
            "notif_email",
            "tg_id",
            "notif_tg",
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
            "notif_email",
            "tg_id",
            "notif_tg",
        )
