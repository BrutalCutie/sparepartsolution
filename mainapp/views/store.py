from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from mainapp.forms import StoreCreateForm
from mainapp.models import Store


class StoreCreateView(CreateView):
    """
    Представление создания магазина
    """

    model = Store
    form_class = StoreCreateForm
    template_name = "mainapp/stores/store-create.html"
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):
        store = form.save()
        user = self.request.user
        user.is_seller = True
        user.store = store

        store.save()
        user.save()

        return super().form_valid(form)


class StoreUpdateView(UpdateView):
    """
    Представление редактирование магазина
    """
    model = Store
    form_class = StoreCreateForm
    template_name = "mainapp/stores/store-create.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user.store


class StoreDeleteView(DeleteView):
    """
    Представление удаления магазина
    """
    model = Store
    template_name = "mainapp/stores/store-delete-confirm.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user.store

    def form_valid(self, form):
        user = self.request.user
        user.is_seller = False
        user.save()

        return super().form_valid(form)
