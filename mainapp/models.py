from django.db import models


class Message(models.Model):
    chat = models.ForeignKey(
        'Chat',
        verbose_name="чат к которому привязано сообщение",
        on_delete=models.CASCADE,
        related_name='chat',
        blank=True,
        null=True,
    )
    message_text = models.TextField(
        verbose_name='текст сообщения',

    )
    image = models.ImageField(
        verbose_name="фото сообщения",
        upload_to=f'media/photos/message_photos/',
        null=True,
        blank=True,

    )
    from_user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="от",
        related_name='messages_from',
        null=True,
        blank=True,

    )
    to_user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="кому",
        related_name='messages_to',
        null=True,
        blank=True,
    )
    sended_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='время отправки',
        null=True,
        blank=True,
    )
    readed = models.BooleanField(
        verbose_name="признак просмотрености",
        default=False
    )

    def __str__(self):
        return f"{self.pk} | from: {self.from_user.pk} | to: {self.to_user.pk}"

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"


class Request(models.Model):

    owner = models.ForeignKey(
        "users.User",
        verbose_name='Создатель заявки',
        on_delete=models.CASCADE,
        related_name='requests',
        null=True,
        blank=True,

    )
    car = models.CharField(
        verbose_name='марка',
        max_length=30,
    )
    model = models.CharField(
        verbose_name='модель',
        max_length=30,
        default="",
    )
    year = models.PositiveSmallIntegerField(
        verbose_name="год",
        null=True,
        blank=True,
        default=None,

    )
    city = models.CharField(
        verbose_name="город",
        help_text="укажите город, если хотите уменьшить количество поступаемых предложений",
        blank=True,
        null=True,
        max_length=30
    )
    city_not_matter = models.BooleanField(
        verbose_name='Город не важен',
        help_text="город в поле выше учитываться не будет",
        blank=True,
    )

    text = models.TextField(
        verbose_name="текст заявки",
    )
    photo = models.ImageField(
        verbose_name='фотографии заявки',
        blank=True,
        null=True,
        upload_to="request_photos/",

    )
    is_active = models.BooleanField(
        verbose_name="признак активной заявки",
        default=False,

    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='время создания заявки',
        null=True
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
        related_name='chats'
    )
    is_active = models.BooleanField(
        verbose_name="признак активности",
        default=False,
    )
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name='инициатор чата',
        default=None,
        blank=True,
        null=True,
    )
    last_updated = models.DateTimeField(
        verbose_name='дата последнего обновления',
        auto_now=True,
        null=True
    )

    def __str__(self):
        return f"pk: {self.pk} | request owner pk {self.request.owner.pk} | created_by user pk {self.created_by.pk} "

    class Meta:
        verbose_name = "чат"
        verbose_name_plural = "чаты"


class Filter(models.Model):
    filter_word = models.CharField(
        max_length=100,
        verbose_name="фильтрующее слово",

    )

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "фильтр уведомления"
        verbose_name_plural = "фильтр уведомления"


class Review(models.Model):
    seller = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="продавец",
        related_name="reviews"
    )
    rating = models.FloatField(verbose_name='оценка')
    review_text = models.TextField(verbose_name="текст отзыва")
    reviewer = models.ForeignKey(
        "users.User",
        verbose_name="ревьювер",
        related_name="writed_reviews",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"PK: {self.pk} | Seller: {self.seller}"

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"


class NotifSetting(models.Model):
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="владелец настройки",
        related_name="notif_settings",
    )
    tg_notif = models.BooleanField(
        verbose_name='признак отправки уведомления на telegram',
        default=False,
    )
    email_notif = models.BooleanField(
        verbose_name='признак отправки уведомления на email',
        default=False,
    )

    def __str__(self):
        return f"PK: {self.pk} | Owner: {self.owner}"

    class Meta:
        verbose_name = "настройка уведомлений"
        verbose_name_plural = "настройки уведомлений"


class Store(models.Model):
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="владелец магазина",
    )
    city = models.CharField(
        verbose_name="город магазина",
        max_length=30,
    )
    address = models.CharField(
        verbose_name="адрес магазина",
        max_length=100,
    )

    def __str__(self):
        return f"PK: {self.pk} | Owner: {self.owner}"

    class Meta:
        verbose_name = "магазин"
        verbose_name_plural = "магазины"
