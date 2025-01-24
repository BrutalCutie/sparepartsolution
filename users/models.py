from django.db import models
from django.contrib.auth.models import AbstractUser

from mainapp.models import Store, Filter


class User(AbstractUser):
    name = models.CharField(
        max_length=200,
        verbose_name='имя',

    )
    tg_id = models.CharField(
        max_length=20,
        verbose_name='ID телеграма',

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
        Store,
        verbose_name='магазин',
        null=True,
        blank=True,
        on_delete=models.CASCADE,

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

    )
    image = models.ImageField(
        verbose_name="аватар",
        upload_to='media/users/',

    )


    def __str__(self):
        return f"{self.pk} | {self.username} | is_seller: {self.is_seller}"

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
