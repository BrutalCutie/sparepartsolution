from django.views.generic import CreateView, UpdateView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404

from users.forms import UserRegistrationsForm, UserUpdateForm
from users.models import User, RegisterConfirmToken
from users.services import UserService


class UserCreateView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegistrationsForm
    success_url = reverse_lazy('users:confirm-email')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        host = self.request.get_host()
        UserService.send_confirm_mail_message(user.pk, host)

        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'users/register.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def email_confirm(request, token):
    register_token = get_object_or_404(RegisterConfirmToken, token=token)
    user = get_object_or_404(User, pk=register_token.user.pk)
    user.is_active = True
    user.save()
    register_token.delete()
    return redirect(f"users:success-email-confirmation")
