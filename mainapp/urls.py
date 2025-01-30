from mainapp import views

from mainapp.apps import MainappConfig

from django.urls import path
from django.views.generic import TemplateView

app_name = MainappConfig.name

urlpatterns = [
    path("", TemplateView.as_view(template_name='mainapp/home.html'), name='home'),

    path("request/create/", views.RequestCreateView.as_view(), name='request-create'),
    path("request/list/", views.RequestListView.as_view(), name='requests-list'),
    path("request/my_requests/", views.MyRequestListView.as_view(), name='my-requests-list'),
    path("request/update/<int:pk>/", views.RequestUpdateView.as_view(), name='request-update'),
    path("request/detail/<int:pk>/", views.RequestDetailView.as_view(), name='request-detail'),
    path("request/delete/<int:pk>/", views.RequestDeleteView.as_view(), name='request-delete'),


]
