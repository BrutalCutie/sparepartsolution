from django.forms import ModelForm

from mainapp.models import Chat, Filter, Message, Request, Store


class RequestCreateForm(ModelForm):
    """
    Форма создания заявки
    """
    class Meta:
        model = Request
        fields = (
            "car",
            "model",
            "year",
            "city",
            "city_not_matter",
            "text",
            "photo",
        )


class ChatCreateForm(ModelForm):
    """
    Форма создания чата
    """

    class Meta:
        model = Chat

        fields = (
            "request",
            "is_active",
            "created_by",
        )


class MessageCreateForm(ModelForm):
    """
    Форма создания сообщения
    """

    class Meta:
        model = Message

        fields = (
            "message_text",
            "image",
        )


class StoreCreateForm(ModelForm):
    """
    Форма создания и редактирования магазина
    """
    class Meta:
        model = Store

        fields = (
            "city",
            "address",
            "name",
        )


class FilterUpdateForm(ModelForm):
    """
    Форма создания фильтра уведомления
    """
    class Meta:
        model = Filter

        fields = ("filter_word",)
