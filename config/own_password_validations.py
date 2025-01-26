from django.utils.translation import ngettext

from django.contrib.auth.password_validation import MinimumLengthValidator
from django.core.exceptions import ValidationError


class OwnPassValidator(MinimumLengthValidator):
    def __init__(self, min_length=12):
        super().__init__(min_length)

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "Пароль слишком короткий. Пароль должен состоять минимум из %(min_length)d символ.",
                    "Пароль слишком короткий. Пароль должен состоять минимум из %(min_length)d символов.",
                    self.min_length,
                ),
                code="password_too_short",
                params={"min_length": self.min_length},
            )

    def get_help_text(self):
        return ngettext(
            "Пароль должен состоять минимум из %(min_length)d символ.",
            "Пароль должен состоять минимум из %(min_length)d символов.",
            self.min_length,
        ) % {"min_length": self.min_length}
