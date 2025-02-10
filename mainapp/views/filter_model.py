from mainapp.models import Filter
from users.models import User
from django.views.generic.edit import CreateView, UpdateView
from mainapp.forms import FilterUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class FilterUpdateView(LoginRequiredMixin, UpdateView):
    model = Filter
    template_name = 'mainapp/filters/filter-create.html'
    form_class = FilterUpdateForm

    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        user = self.request.user
        filter_model = user.filter

        if not filter_model:
            filter_model = Filter.objects.create(
                filter_word='',
            )
            user.filter = filter_model
            user.save()

        return filter_model
