from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import DetailView, ListView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from mainapp.mixins import IsChatMember
from mainapp.models import Chat, Message
from mainapp.serializers import ChatSerializer


class ChatListApiView(generics.ListAPIView):
    """
    Представление получения списка чатов пользователя по API.
    Возвращает только списки чатов, что пользователь является участником.
    """
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    queryset = Chat.objects.all()

    def get_queryset(self):
        user = self.request.user

        queryset = Chat.objects.filter(Q(request__owner=user) | Q(created_by=user))

        return queryset


class ChatListView(LoginRequiredMixin, ListView):
    """
    Представление списка чатов.
    Возвращает чаты, в которых пользователь является участником.
    Так-же представление выявляет, есть ли непрочитанные сообщения.
    """
    model = Chat
    template_name = "mainapp/chats/chat-list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context["unreaded"] = list()  # список для чатов, где есть непрочитанные сообщения
        user = self.request.user
        chats = Chat.objects.filter(Q(request__owner=user) | Q(created_by=user))

        for chat in chats:
            unreaded_messages = Message.objects.filter(chat__pk=chat.pk, to_user=user, readed=False)

            if unreaded_messages:  # если в чате есть непрочитанные сообщения, добавляем в список
                context["unreaded"].append(chat.pk)

        # сортируем чаты по последнему обновлению
        context["chats"] = chats.order_by("-last_updated")
        return context


class ChatDetailView(LoginRequiredMixin, IsChatMember, DetailView):
    """
    Представление чата и получение сообщений, относящихся к чату.
    """
    model = Chat
    template_name = "mainapp/chats/chat-detail.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context["unreaded"] = list()
        user = self.request.user
        chats = Chat.objects.filter(Q(request__owner=user) | Q(created_by=user))
        messages = Message.objects.filter(chat__pk=self.kwargs["pk"])
        messages.filter(to_user=user).update(readed=True)

        for chat in chats:
            unreaded_messages = Message.objects.filter(chat__pk=chat.pk, to_user=user, readed=False)
            if unreaded_messages:
                context["unreaded"].append(chat.pk)

        context["chats"] = chats.order_by("-last_updated")
        context["messages"] = messages.order_by("sended_at")
        context["request_model"] = messages.first().chat.request
        return context
