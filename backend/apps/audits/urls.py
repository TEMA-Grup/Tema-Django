from django.urls import path
from . import views

urlpatterns = [
    path("", views.audits_home, name="audits_home"),
]
