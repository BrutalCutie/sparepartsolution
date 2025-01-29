from mainapp import views

from mainapp.apps import MainappConfig

from django.urls import path
from django.views.generic import TemplateView

app_name = MainappConfig.name

urlpatterns = [
    path("", TemplateView.as_view(template_name='mainapp/home.html'), name='home'),

]
