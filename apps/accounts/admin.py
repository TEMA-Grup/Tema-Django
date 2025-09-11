from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

User = get_user_model()
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "is_active", "is_staff", "active_company")
    list_filter = ("is_active", "is_staff", "is_superuser", "groups")
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Company", {"fields": ("companies", "active_company")}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ("Company", {"fields": ("companies", "active_company")}),
    )
    filter_horizontal = ("groups", "user_permissions", "companies")