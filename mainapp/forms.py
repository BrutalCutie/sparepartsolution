from django.forms import ModelForm

from mainapp.models import Request


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
