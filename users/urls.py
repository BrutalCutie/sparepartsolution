from users import views

from users.apps import UsersConfig

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView


app_name = UsersConfig.name

urlpatterns = [
    path("register/", views.UserCreateView.as_view(), name='register'),
    path("login/", LoginView.as_view(template_name="users/login.html"), name='login'),
    path("logout/", LogoutView.as_view(next_page='mainapp:index'), name='logout'),

]
