from django.db import models
from django.contrib.auth.models import AbstractUser

from mainapp.models import Filter


class User(AbstractUser):
    name = models.CharField(
        max_length=200,
        verbose_name='имя',

    )
    tg_id = models.CharField(
        max_length=20,
        verbose_name='ID телеграма',
        null=True,
        blank=True,

    )
    username = models.CharField(
        max_length=100,
        verbose_name='псевдоним',
        null=True,
        blank=True,
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="номер телефона",

    )
    email = models.EmailField(
        verbose_name="почта",
        unique=True,

    )
    is_seller = models.BooleanField(
        verbose_name='признак продавца',
        default=False,
        null=True,
        blank=True,
    )
    store = models.ForeignKey(
        'mainapp.Store',
        on_delete=models.CASCADE,
        verbose_name='магазин пользователя',
        null=True,
        blank=True,
        default=None,
    )

    filter = models.ForeignKey(
        Filter,
        verbose_name='фильтр уведомлений',
        on_delete=models.CASCADE,
        blank=True,
        null=True,

    )
    rating = models.FloatField(
        verbose_name='рейтинг продавца',
        null=True,
        blank=True,

    )
    image = models.ImageField(
        verbose_name="аватар",
        upload_to='users/avatars/',
        null=True,
        blank=True,
        default='/users/avatars/wo-avatar.png'

    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='признак активности',

    )
    notif_tg = models.BooleanField(
        verbose_name="Уведомления в Telegram",
        blank=True,
        default=False,
    )
    notif_email = models.BooleanField(
        verbose_name="Уведомления по почте",
        blank=True,
        default=False,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone", "username"]

    def __str__(self):
        return f"{self.pk} | {self.name} | is_seller: {self.is_seller}"

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class RegisterConfirmToken(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='register_token',
        verbose_name='токен регистрации'
    )
    token = models.CharField(max_length=40)
