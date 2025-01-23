from django.db import models


class Request(models.Model):

    def __str__(self):
        pass

    class Meta:
        verbose_name = "заявка"
        verbose_name_plural = "заявки"


class Chat(models.Model):

    def __str__(self):
        pass

    class Meta:
        verbose_name = "чат"
        verbose_name_plural = "чаты"


class Message(models.Model):

    def __str__(self):
        pass

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"


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
