from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from mainapp.models import Request, Chat
from mainapp.forms import ChatCreateForm


class ChatCreateView(CreateView):
    form_class = ChatCreateForm


class ChatListView(ListView):
    pass


class ChatDetailView(DetailView):
    pass


class ChatUpdateView(UpdateView):
    pass


class ChatDeleteView(DeleteView):
    pass
