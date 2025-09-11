from django.urls import path
from . import views
from apps.core.views_auth import LogoutViewAllowGet
urlpatterns = [
    path("", views.accounts_home, name="accounts_home"),
    path("logout/", LogoutViewAllowGet.as_view(next_page="login"), name="logout")
]
