from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from mainapp.models import Request, Chat, Message
from mainapp.forms import ChatCreateForm
from django.db.models import Q


class ChatListView(ListView):
    model = Chat
    template_name = 'mainapp/chats/chat-list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        user = self.request.user
        chats = Chat.objects.filter(Q(request__owner=user) | Q(created_by=user))
        context['chats'] = chats
        return context


class ChatDetailView(DetailView):
    model = Chat
    template_name = 'mainapp/chats/chat-detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        user = self.request.user
        chats = Chat.objects.filter(Q(request__owner=user) | Q(created_by=user))
        messages = Message.objects.all()
        context['chats'] = chats
        context['messages'] = messages

        return context
