from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from mainapp.models import Request, Chat, Message
from mainapp.forms import MessageCreateForm
from django.shortcuts import get_object_or_404
from django.db.models import Q


class MessageCreateView(CreateView):
    template_name = "mainapp/messages/message-create.html"
    form_class = MessageCreateForm

    def form_valid(self, form):
        message = form.save()
        request_pk = self.kwargs.get('pk')
        request = get_object_or_404(Request, pk=request_pk)
        user = self.request.user
        chat = Chat.objects.filter(Q(request__owner=user) | Q(created_by=user)).first()
        if not chat:
            chat = Chat.objects.create(
                is_active=True,
                created_by=self.request.user,
                request=request,
            )
        message.chat = chat
        message.to_user = chat.request.owner
        message.from_user = self.request.user

        message.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.kwargs

        return context

    def get_success_url(self):
        return reverse('mainapp:request-detail', kwargs={'pk': self.kwargs.get('pk')})


class MessageListView(ListView):
    pass


class MessageDetailView(DetailView):
    pass


class MessageUpdateView(UpdateView):
    pass


class MessageDeleteView(DeleteView):
    pass
