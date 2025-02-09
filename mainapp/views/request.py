from django.views.generic import ListView, DetailView, DeleteView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from mainapp.models import Request, Chat
from mainapp.forms import RequestCreateForm
from users.tasks import send_new_request_notifications


class RequestCreateView(LoginRequiredMixin, CreateView):
    template_name = "mainapp/requests/request-create.html"
    form_class = RequestCreateForm

    success_url = reverse_lazy('mainapp:my-requests-list')

    def form_valid(self, form):
        request = form.save()
        user = self.request.user
        request.owner = user
        if request.city_not_matter or not request.city:
            request.city = 'Все города'
        request.save()

        send_new_request_notifications.delay(request_id=request.pk)

        return super().form_valid(form)


class RequestListView(ListView):
    model = Request
    template_name = "mainapp/requests/requests-list.html"
    context_object_name = "requests"


class MyRequestListView(RequestListView):

    def get_queryset(self):
        my_requests = Request.objects.filter(owner=self.request.user)

        return my_requests


class RequestDetailView(DetailView):
    model = Request
    template_name = "mainapp/requests/request-detail.html"
    context_object_name = 'request_model'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['chat_exists'] = Chat.objects.filter(created_by=user, request=self.object.pk).first()

        return context


class RequestUpdateView(UpdateView):
    template_name = "mainapp/requests/request-create.html"
    model = Request
    form_class = RequestCreateForm

    def get_success_url(self):
        return reverse("mainapp:request-detail", kwargs={"pk": self.object.pk})


class RequestDeleteView(DeleteView):
    model = Request
    template_name = "mainapp/requests/request-delete-confirm.html"
    success_url = reverse_lazy("mainapp:my-requests-list")
