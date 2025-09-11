from django.urls import path
from . import views

urlpatterns = [
    path("", views.companies_home, name="companies_home"),
]
