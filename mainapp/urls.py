from mainapp import views

from mainapp.apps import MainappConfig

from django.urls import path

app_name = MainappConfig.name

urlpatterns = [
    path("", views.HomePage.as_view(), name='index'),

]
