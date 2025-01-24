from django.db import models

from users.models import User


class Message(models.Model):
    chat = models.ForeignKey(
        'Chat',
        verbose_name="чат к которому привязано сообщение",
        on_delete=models.CASCADE,

    )
    message_text = models.TextField(
        verbose_name='текст сообщения',

    )
    image = models.ImageField(
        verbose_name="фото сообщения",
        upload_to=f'media/photos/message_photos/'

    )
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="от"

    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="кому"
    )

    def __str__(self):
        return f"{self.pk} | from: {self.from_user} | to: {self.to_user}"

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"


class Request(models.Model):

    owner = models.ForeignKey(
        User,
        verbose_name='Создатель заявки',
        on_delete=models.CASCADE,
        related_name='requests',

    )
    request_text = models.TextField(
        verbose_name="текст заявки",

    )
    request_photo = models.ImageField(
        verbose_name='фотографии заявки',
        blank=True,
        null=True,
        upload_to="media/request_photos/",

    )
    is_active = models.BooleanField(
        verbose_name="признак активной заявки",
        default=False,

    )

    def __str__(self):
        return f"{self.pk} | {self.owner}"

    class Meta:
        verbose_name = "заявка"
        verbose_name_plural = "заявки"


class Chat(models.Model):
    request = models.ForeignKey(
        Request,
        verbose_name='заявка',
        on_delete=models.CASCADE,


    )
    messages = models.ManyToManyField(
        Message,
        verbose_name='сообщения чата',
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        verbose_name="признак активности",
        default=False,

    )


    def __str__(self):
        pass

    class Meta:
        verbose_name = "чат"
        verbose_name_plural = "чаты"


class Filter(models.Model):

    def __str__(self):
        pass

    class Meta:
        verbose_name = "фильтр уведомления"
        verbose_name_plural = "фильтр уведомления"


class Review(models.Model):

    def __str__(self):
        pass

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"


class NotifSetting(models.Model):

    def __str__(self):
        pass

    class Meta:
        verbose_name = "настройка уведомлений"
        verbose_name_plural = "настройки уведомлений"


class Store(models.Model):

    def __str__(self):
        pass

    class Meta:
        verbose_name = "магазин"
        verbose_name_plural = "магазины"
