from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from users.models import User


class UserRegistrationsForm(UserCreationForm):
    """
    Форма создания пользователя
    """
    class Meta:
        model = User
        fields = (
            "name",
            "phone",
            "email",
            "tg_id",
            "notif_email",
            "notif_tg",
            "password1",
            "password2",
        )


class UserUpdateForm(UserChangeForm):
    """
    Форма редактирования пользователя
    """
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
