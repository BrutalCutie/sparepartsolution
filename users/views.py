from django.views.generic import CreateView
from django.urls import reverse_lazy

from users.forms import UserRegistrationsForm


class UserCreateView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegistrationsForm
    success_url = reverse_lazy('users:login')
