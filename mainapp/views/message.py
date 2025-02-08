from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from mainapp.models import Request, Chat, Message
from mainapp.forms import MessageCreateForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from users.tasks import send_new_message_notification


class MessageCreateView(CreateView):
    template_name = "mainapp/messages/message-create.html"
    form_class = MessageCreateForm

    def form_valid(self, form):

        message = form.save()
        request_pk = self.kwargs.get('pk')
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
        self.kwargs['redirect_to_chat_pk'] = chat.pk

        send_new_message_notification.delay(user_id=message.to_user.id, message_id=message.id)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.kwargs

        return context

    def get_success_url(self):
        return reverse('mainapp:chat-detail', kwargs={'pk': self.kwargs.get('redirect_to_chat_pk')})


class ChatNewMessage(LoginRequiredMixin, CreateView):
    template_name = "mainapp/messages/new-chat-message.html"
    form_class = MessageCreateForm
    
    def form_valid(self, form):
        message = form.save()
        chat = Chat.objects.get(pk=self.kwargs['pk'])
        chat.save()
        user = self.request.user
        message.chat = chat
        message.from_user = user

        if user == chat.request.owner:
            message.to_user = chat.created_by
        else:
            message.to_user = chat.request.owner
        message.save()

        host = self.request.get_host()
        send_new_message_notification.delay(user_id=message.to_user.id, message_id=message.id, host=host)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mainapp:chat-detail', kwargs={'pk': self.kwargs.get('pk')})
