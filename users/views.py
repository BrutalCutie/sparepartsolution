from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from users.forms import UserRegistrationsForm, UserUpdateForm
from users.models import RegisterConfirmToken, User
from users.services import UserService


class UserCreateView(CreateView):
    """
    Представление отвечающее за создание пользователя
    """
    template_name = "users/register.html"
    form_class = UserRegistrationsForm
    # Не возвращаем success_url а рендерим страницу

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        host = self.request.get_host()
        UserService.send_confirm_mail_message(user.pk, host)
        return render(self.request, "users/confirm_email.html")


class UserProfileView(LoginRequiredMixin, TemplateView):
    """
    Представление отвечающее за просмотр профиля пользователя
    """
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.filter and user.filter.filter_word:
            user_filters = [x for x in user.filter.filter_word.split("\r\n")]
            context["user_filters"] = ", ".join(user_filters)

        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление отвечающее за редактирования данных пользователя
    """
    template_name = "users/register.html"
    form_class = UserUpdateForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):

        user = form.save()

        # Если пользователь удалил (галочка "Clear") фото профиля
        if not user.image:
            # Назначаем фото профиля default значением модели User
            user.image = User.image.field.default

        user.save()

        return super().form_valid(form)


def email_confirm(request, token):
    """
    Функция для подтверждения почты пользователя, при переходе по ссылке
    """
    register_token = RegisterConfirmToken.objects.filter(token=token)
    if not register_token.exists() and request.method == "GET":
        return render(request, "mainapp/wrong_register_token.html")
    user = get_object_or_404(User, register_token=register_token.first())
    user.is_active = True
    user.save()
    register_token.delete()
    return redirect("users:success-email-confirmation")
