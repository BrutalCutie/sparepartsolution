import requests
from celery import shared_task

from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER, TG_BOT_TOKEN, SERVICE_NAME
from mainapp.models import Message
from users.models import User


@shared_task
def send_email_confirmation_url(data: dict):
    send_mail(
        subject=data.get("subject"),
        message=data.get("message_text"),
        from_email=EMAIL_HOST_USER,
        recipient_list=[data.get("user_email")],
    )


@shared_task
def send_new_message_notification(user_id: int, message_id: int, host: str):
    user = User.objects.get(pk=user_id)
    if user.notif_tg:
        send_new_message_telegram_notification.delay(message_id=message_id, host=host)
    if user.notif_email:
        send_new_message_email_notification.delay(message_id=message_id, host=host)


@shared_task
def send_new_message_telegram_notification(message_id: int, host: str):

    message = Message.objects.get(pk=message_id)
    store_or_user = message.from_user.store.name if message.from_user.is_seller else message.from_user.name
    start_message_text = f"Вам пришло новое сообщение от <b>{store_or_user}</b>\n\n"
    end_message_text = f'\n\nПерейти в чат - {host}/chat/detail/{message.chat.pk}/\n\nКоманда {SERVICE_NAME}'

    message_text = start_message_text + message.message_text + end_message_text
    message_to = message.to_user
    receiver_tg_id = message_to.tg_id

    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage?chat_id={receiver_tg_id}&text={message_text}&parse_mode=HTML"
    requests.get(url)


@shared_task
def send_new_message_email_notification(message_id: int, host):
    subject = "Вам пришло одно новое сообщение от продавца"
    message = Message.objects.get(pk=message_id)
    store_or_user = message.from_user.store.name if message.from_user.is_seller else message.from_user.name
    start_message_text = f"Вам пришло одно новое сообщение от {store_or_user}\n\n"
    end_message_text = f'\n\nПерейти в чат - {host}/chat/detail/{message.chat.pk}/\n\nКоманда {SERVICE_NAME}'
    message_text = start_message_text + message.message_text + end_message_text
    result = send_mail(
        subject=subject,
        message=message_text,
        from_email=EMAIL_HOST_USER,
        recipient_list=[message.to_user.email],
    )

    if result in [1, '1']:
        print(f"Сообщение успешно ушло на почту {message.to_user.email}")
    else:
        print(f"Что-то пошло не так. send_main вернул {result}")


