from celery import shared_task

from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


@shared_task
def send_email_confirmation_url(data: dict):
    send_mail(
        subject=data.get("subject"),
        message=data.get("message_text"),
        from_email=EMAIL_HOST_USER,
        recipient_list=[data.get("user_email")],
    )
