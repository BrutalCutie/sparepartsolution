from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.edit import CreateView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from mainapp.forms import MessageCreateForm
from mainapp.mixins import IsSellerMixin
from mainapp.models import Chat, Message, Request
from mainapp.permissions import IsChatMember
from mainapp.serializers import MessageSerializer
from users.tasks import send_new_message_notification


class MessageListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsChatMember]
    queryset = Message.objects.all()

    def get_queryset(self):

        queryset = Message.objects.filter(chat=self.kwargs.get("chat_pk")).order_by("-sended_at")

        return queryset


class MessageCreateView(LoginRequiredMixin, IsSellerMixin, CreateView):
    template_name = "mainapp/messages/message-create.html"
    form_class = MessageCreateForm

    def form_valid(self, form):

        message = form.save()
        request_pk = self.kwargs.get("pk")
        request = get_object_or_404(Request, pk=request_pk)
        user = self.request.user
        chat = Chat.objects.filter(request__owner=request.owner, created_by=user, request=request).first()
        if not chat:
            chat = Chat.objects.create(
                is_active=True,
                created_by=self.request.user,
                request=request,
            )
        message.chat = chat
        message.to_user = chat.request.owner
        message.from_user = user
        message.save()
        self.kwargs["redirect_to_chat_pk"] = chat.pk

        send_new_message_notification.delay(user_id=message.to_user.id, message_id=message.id)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request"] = self.kwargs

        return context

    def get_success_url(self):
        return reverse("mainapp:chat-detail", kwargs={"pk": self.kwargs.get("redirect_to_chat_pk")})


class ChatNewMessage(LoginRequiredMixin, IsSellerMixin, CreateView):
    template_name = "mainapp/messages/new-chat-message.html"
    form_class = MessageCreateForm

    def form_valid(self, form):
        message = form.save()
        chat = Chat.objects.get(pk=self.kwargs["pk"])
        chat.save()
        user = self.request.user
        message.chat = chat
        message.from_user = user

        if user == chat.request.owner:
            message.to_user = chat.created_by
        else:
            message.to_user = chat.request.owner
        message.save()
        send_new_message_notification.delay(user_id=message.to_user.id, message_id=message.id)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("mainapp:chat-detail", kwargs={"pk": self.kwargs.get("pk")})
