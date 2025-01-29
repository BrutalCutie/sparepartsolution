import secrets

from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER, SERVICE_NAME
from users.models import User, RegisterConfirmToken


class UserService:

    @staticmethod
    def send_confirm_mail_message(user_id, host):
        token = secrets.token_hex(16)
        user = User.objects.get(id=user_id)
        RegisterConfirmToken.objects.create(
            user=user,
            token=token,

        )
        url = f"http://{host}/users/success-email-confirmation/{token}"

        subject = f"Подтверждение почты {SERVICE_NAME}"
        message_text = f"Для получения доступа к сервису, пройдите пожалуйста по ссылке ниже:\n\n{url}"

        send_mail(
            subject=subject,
            message=message_text,
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
