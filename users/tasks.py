import requests
from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Q

from config.settings import BASE_HOST, EMAIL_HOST_USER, SERVICE_NAME, TG_BOT_TOKEN
from mainapp.models import Message, Request
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
def send_new_message_notification(user_id: int, message_id: int):
    user = User.objects.get(pk=user_id)
    if user.notif_tg:
        send_new_message_telegram_notification.delay(message_id=message_id)
    if user.notif_email:
        send_new_message_email_notification.delay(message_id=message_id)


@shared_task
def send_new_message_telegram_notification(message_id: int):

    message = Message.objects.get(pk=message_id)
    store_or_user = message.from_user.store.name if message.from_user.is_seller else message.from_user.name
    start_message_text = f"Вам пришло новое сообщение от <b>{store_or_user}</b>\n\n"
    end_message_text = f"\n\nПерейти в чат - {BASE_HOST}/chat/detail/{message.chat.pk}/\n\nКоманда {SERVICE_NAME}"

    message_text = start_message_text + message.message_text + end_message_text
    message_to = message.to_user
    receiver_tg_id = message_to.tg_id

    url = (
        f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage?"
        f"chat_id={receiver_tg_id}&"
        f"text={message_text}&"
        f"parse_mode=HTML"
    )
    requests.get(url)


@shared_task
def send_new_message_email_notification(message_id: int):
    subject = "Вам пришло одно новое сообщение от продавца"
    message = Message.objects.get(pk=message_id)
    store_or_user = message.from_user.store.name if message.from_user.is_seller else message.from_user.name
    start_message_text = f"Вам пришло одно новое сообщение от {store_or_user}\n\n"
    end_message_text = f"\n\nПерейти в чат - {BASE_HOST}/chat/detail/{message.chat.pk}/\n\nКоманда {SERVICE_NAME}"
    message_text = start_message_text + message.message_text + end_message_text
    send_mail(
        subject=subject,
        message=message_text,
        from_email=EMAIL_HOST_USER,
        recipient_list=[message.to_user.email],
    )


@shared_task
def send_new_request_email_notification(request_id: int, user_id: int):
    subject = "Вам пришло одно новое сообщение от продавца"
    request = Request.objects.get(pk=request_id)

    user_to_notify = User.objects.get(pk=user_id)

    start_message_text = (
        f"Поступила новая заявка\n\n" f"<b>{request.car} {request.car} {request.year}</b>\n\n" f"{request.text}"
    )
    end_message_text = f"\n\nК заявке - {BASE_HOST}/request/detail/{request.pk}/\n\nКоманда {SERVICE_NAME}"
    message_text = start_message_text + request.text + end_message_text
    send_mail(
        subject=subject,
        message=message_text,
        from_email=EMAIL_HOST_USER,
        recipient_list=[user_to_notify.email],
    )


@shared_task
def send_new_request_telegram_notification(request_id: int, user_id: int):
    request = Request.objects.get(pk=request_id)
    user_to_notify = User.objects.get(pk=user_id)

    start_message_text = f"Поступила новая заявка\n\n{request.car} {request.car} {request.year}\n\n{request.text}"
    end_message_text = f"\n\nК заявке - {BASE_HOST}/request/detail/{request.pk}/"

    message_text = start_message_text + request.text + end_message_text
    receiver_tg_id = user_to_notify.tg_id

    url = (f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage?"
           f"chat_id={receiver_tg_id}&"
           f"text={message_text}&"
           f"parse_mode=HTML")
    requests.get(url)


@shared_task
def send_new_request_notifications(request_id: int):
    users = User.objects.filter(Q(notif_tg=True) | Q(notif_email=True), is_seller=True, is_active=True)

    request = Request.objects.get(pk=request_id)
    request_text = f"{request.car} {request.model} {request.year} {request.city}. {request.text}".lower()

    for user in users:
        is_need_notify = True

        if user.filter and user.filter.filter_word != "":
            filter_words_parts = user.filter.filter_word.split("\r\n")
            filter_words = [x.lower() for x in filter_words_parts]
            is_need_notify = any([x in request_text for x in filter_words])

        if is_need_notify:
            if user.notif_email:
                send_new_request_email_notification.delay(request_id=request.pk, user_id=user.pk)
            if user.notif_tg:
                send_new_request_telegram_notification.delay(request_id=request.pk, user_id=user.pk)
