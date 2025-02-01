from django.forms import ModelForm

from mainapp.models import Request, Chat


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
