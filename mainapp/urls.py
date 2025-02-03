from mainapp.views import request, chat, message

from mainapp.apps import MainappConfig

from django.urls import path
from django.views.generic import TemplateView

app_name = MainappConfig.name

urlpatterns = [
    path("", TemplateView.as_view(template_name='mainapp/home.html'), name='home'),

    path("request/create/", request.RequestCreateView.as_view(), name='request-create'),
    path("request/list/", request.RequestListView.as_view(), name='requests-list'),
    path("request/my_requests/", request.MyRequestListView.as_view(), name='my-requests-list'),
    path("request/update/<int:pk>/", request.RequestUpdateView.as_view(), name='request-update'),
    path("request/detail/<int:pk>/", request.RequestDetailView.as_view(), name='request-detail'),
    path("request/detail/<int:pk>/new_message/", message.MessageCreateView.as_view(), name='new-message'),
    path("request/delete/<int:pk>/", request.RequestDeleteView.as_view(), name='request-delete'),

    path("chat/list/", chat.ChatListView.as_view(), name='chats-list'),
    path("chat/detail/<int:pk>/", chat.ChatDetailView.as_view(), name='chat-detail'),


]
