from users import views

from users.apps import UsersConfig

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, TemplateView


app_name = UsersConfig.name

urlpatterns = [
    path("register/", views.UserCreateView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("profile-update/", views.UserUpdateView.as_view(), name="profile-update"),
    path("logout/", LogoutView.as_view(next_page='mainapp:home'), name="logout"),
    path("success-email-confirmation/", TemplateView.as_view(template_name='users/success_email_confirmation.html'), name="success-email-confirmation"),
    path("success-email-confirmation/<str:token>/", views.email_confirm, name='success-email-confirmation-token'),

]
