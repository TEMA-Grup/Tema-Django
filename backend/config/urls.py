
from django.contrib import admin
from django.urls import path, include
from apps.core.views_auth import LogoutViewAllowGet

urlpatterns = [
    path("admin/logout/", LogoutViewAllowGet.as_view(next_page="login"), name="admin_logout"),
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("audits/", include("apps.audits.urls")),
    path("companies/", include("apps.companies.urls")),
    path("clients/", include("apps.clients.urls")),
    
    path("accounts/", include("django.contrib.auth.urls")),
    
    path("accounts/", include("apps.accounts.urls")),
    path("billing/", include("apps.billing.urls")),
]
