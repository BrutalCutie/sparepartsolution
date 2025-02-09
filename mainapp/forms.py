from django.forms import ModelForm

from mainapp.models import Request, Chat, Message, Store, Filter


class RequestCreateForm(ModelForm):

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

    class Meta:
        model = Chat

        fields = (
            "request",
            "is_active",
            "created_by",

        )


class MessageCreateForm(ModelForm):

    class Meta:
        model = Message

        fields = (
            "message_text",
            "image",
        )


class StoreCreateForm(ModelForm):

    class Meta:
        model = Store

        fields = (
            "city",
            "address",
            "name",
        )


class FilterUpdateForm(ModelForm):

    class Meta:
        model = Filter

        fields = (
            "filter_word",
        )
