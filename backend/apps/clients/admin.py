from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "email", "phone")
    list_filter = ("company",)
    search_fields = ("name", "email", "phone")
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        ac = getattr(request.user, "active_company_id", None)
        if ac:
            return qs.filter(company_id=ac)
        return qs.filter(company__in=request.user.companies.all()).distinct()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "company" and not request.user.is_superuser:
            ac = getattr(request.user, "active_company_id", None)
            if ac:
                kwargs["queryset"] = kwargs["queryset"].filter(id=ac)
            else:
                kwargs["queryset"] = kwargs["queryset"].filter(users=request.user).distinct()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)