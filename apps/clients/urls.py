from django.urls import path
from . import views

urlpatterns = [
    path("", views.clients_home, name="clients_home"),
]
