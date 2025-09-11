from django.contrib import admin
from .models import Company, Sector

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "legal_title", "sector", "staff_count", "founded_year", "vat_number")
    search_fields = ("name", "legal_title", "vat_number")
    list_filter = ("sector", "founded_year")
    fieldsets = (
        ("Genel1", {"fields": ("name", "legal_title", "sector")}),
        ("Resmî Bilgiler", {"fields": ("vat_number", "founded_year", "staff_count")}),
    )