from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

from mainapp.forms import FilterUpdateForm
from mainapp.models import Filter


class FilterUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление отвечающее как за создание фильтра уведомлений,
    так и за редактирование фильтра
    """
    model = Filter
    template_name = "mainapp/filters/filter-create.html"
    form_class = FilterUpdateForm

    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        user = self.request.user
        filter_model = user.filter

        if not filter_model:  # при отсутствии фильтра - создаем его
            filter_model = Filter.objects.create(
                filter_word="",
            )
            user.filter = filter_model
            user.save()

        return filter_model
