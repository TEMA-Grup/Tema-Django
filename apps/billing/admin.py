from django.contrib import admin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("number", "customer_name", "amount", "status", "issue_date", "company")
    list_filter = ("status", "company")
    search_fields = ("number", "customer_name")