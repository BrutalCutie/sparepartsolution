import secrets

from config.settings import SERVICE_NAME
from users.models import RegisterConfirmToken, User
from users.tasks import send_email_confirmation_url


class UserService:

    @staticmethod
    def send_confirm_mail_message(user_id, host):
        token = secrets.token_hex(16)
        user = User.objects.get(id=user_id)
        RegisterConfirmToken.objects.create(
            user=user,
            token=token,
        )

        data = {
            "user_email": user.email,
            "url": f"http://{host}/users/success-email-confirmation/{token}",
            "subject": f"Подтверждение почты {SERVICE_NAME}",
        }

        data["message_text"] = f"Для получения доступа к сервису, пройдите пожалуйста по ссылке ниже:\n\n{data['url']}"

        send_email_confirmation_url.delay(data)
