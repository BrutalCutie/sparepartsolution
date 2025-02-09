from django.views.generic.edit import CreateView, UpdateView
from mainapp.forms import StoreCreateForm
from django.urls import reverse_lazy

from mainapp.models import Store


class StoreCreateView(CreateView):
    model = Store
    form_class = StoreCreateForm
    template_name = 'mainapp/stores/store-create.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        store = form.save()
        user = self.request.user
        user.is_seller = True
        user.store = store

        store.save()
        user.save()

        return super().form_valid(form)


class StoreUpdateView(UpdateView):
    model = Store
    form_class = StoreCreateForm
    template_name = 'mainapp/stores/store-create.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user.store
