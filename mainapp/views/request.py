from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from rest_framework import generics

from mainapp.forms import RequestCreateForm
from mainapp.mixins import IsModelOwnerMixin
from mainapp.models import Chat, Request
from mainapp.serializers import RequestSerializer
from users.tasks import send_new_request_notifications


class RequestListAPIView(generics.ListAPIView):
    """
    Представление отдаёт по API список всех открытых заявок
    """
    serializer_class = RequestSerializer
    queryset = Request.objects.filter(is_active=True).order_by("-created_at")


class RequestCreateView(LoginRequiredMixin, CreateView):
    """
    Представление создания заявки
    """
    template_name = "mainapp/requests/request-create.html"
    form_class = RequestCreateForm

    success_url = reverse_lazy("mainapp:my-requests-list")

    def form_valid(self, form):
        request = form.save()
        user = self.request.user
        request.owner = user
        if request.city_not_matter or not request.city:
            request.city = "Все города"
        request.save()
        # отправляем задачу для уведомлений в фон
        send_new_request_notifications.delay(request_id=request.pk)

        # Устанавливаем заявки в кэш, для того чтобы не дёргать
        # базу данных каждое обращение при отсутствии обновлений
        new_cache_set = Request.objects.filter(is_active=True)

        cache.set("requests_set", new_cache_set, 60 * 5)

        return super().form_valid(form)


class RequestListView(ListView):
    """
    Представление отвечающее за выдачу списка заявок
    """
    model = Request
    template_name = "mainapp/requests/requests-list.html"
    context_object_name = "requests"

    def get_queryset(self):
        # Берём список заявок из кэша. Если кэша нет - создаем новый кэшированный список
        queryset = cache.get("requests_set")
        if not queryset:
            queryset = super().get_queryset()
            cache.set("requests_set", queryset.order_by("-created_at"), 60 * 5)

        # забираем данные из строки поиска
        search_field_data = self.request.GET.get("request_search_field")

        if search_field_data:
            return queryset.filter(
                Q(car__icontains=search_field_data.lower()) | Q(model__icontains=search_field_data) | Q(
                    city__icontains=search_field_data) | Q(text__icontains=search_field_data),
                is_active=True,
            )

        return queryset


class MyRequestListView(RequestListView):
    """
    Представление отвечает за выдачу заявок созданных пользователем
    """

    def get_queryset(self):
        my_requests = Request.objects.filter(owner=self.request.user)

        return my_requests


class RequestDetailView(LoginRequiredMixin, DetailView):
    """
    Представление отвечает за выдачу информации по заявке.
    """
    model = Request
    template_name = "mainapp/requests/request-detail.html"
    context_object_name = "request_model"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["chat_exists"] = Chat.objects.filter(created_by=user, request=self.object.pk).first()

        return context


class RequestUpdateView(LoginRequiredMixin, IsModelOwnerMixin, UpdateView):
    """
    Представление отвечает за редактирование заявки, если пользователь владелец заявки
    """
    template_name = "mainapp/requests/request-create.html"
    model = Request
    form_class = RequestCreateForm

    def get_success_url(self):
        cache.delete("requests_set")
        return reverse("mainapp:request-detail", kwargs={"pk": self.object.pk})


class RequestDeleteView(LoginRequiredMixin, IsModelOwnerMixin, DeleteView):
    """
    Представление отвечает за удаление заявки, если пользователь владелец заявки
    """
    model = Request
    template_name = "mainapp/requests/request-delete-confirm.html"

    def form_valid(self, form):
        cache.delete("requests_set")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("mainapp:my-requests-list")
