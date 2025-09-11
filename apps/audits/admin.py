from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Audit, Sequence, Finding, Action, Todo, Attachment

@admin.register(Sequence)
class SequenceAdmin(admin.ModelAdmin):
    list_display = ("company", "code", "prefix", "padding", "last_number")
    list_filter = ("company", "code")
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        ac = getattr(request.user, "active_company_id", None)
        if ac:
            return qs.filter(company_id=ac)
        return qs.filter(company__users=request.user).distinct()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "company" and not request.user.is_superuser:
            ac = getattr(request.user, "active_company_id", None)
            if ac:
                kwargs["queryset"] = kwargs["queryset"].filter(id=ac)
            else:
                kwargs["queryset"] = kwargs["queryset"].filter(users=request.user).distinct()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
class FindingInline(admin.TabularInline):
    model = Finding
    extra = 0
    show_change_link = True
class ActionInline(admin.TabularInline):
    model = Action
    extra = 0
class TodoInline(admin.TabularInline):
    model = Todo
    extra = 0
class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0

@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ("reference", "name", "company", "client", "audit_type", "state", "progress")
    list_filter = ("company", "audit_type", "state")
    search_fields = ("reference", "name")
    list_select_related = ("company", "client", "auditor")
    readonly_fields = ("reference",)
    inlines = [FindingInline, TodoInline, AttachmentInline]
    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related("company", "client")
        if request.user.is_superuser:
            return qs
        ac = getattr(request.user, "active_company_id", None)
        if ac:
            return qs.filter(company_id=ac)
        return qs.filter(company__users=request.user).distinct()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs) 
        ac = getattr(request.user, "active_company_id", None)
        if db_field.name == "company":
            kwargs["queryset"] = kwargs["queryset"].filter(id=ac) if ac else kwargs["queryset"].filter(users=request.user).distinct()
        elif db_field.name == "client":
            kwargs["queryset"] = kwargs["queryset"].filter(company_id=ac) if ac else kwargs["queryset"].filter(company__users=request.user).distinct()
        elif db_field.name == "auditor":
            User = get_user_model()
            kwargs["queryset"] = User.objects.filter(companies__id=ac).distinct() if ac else User.objects.filter(companies__users=request.user).distinct()
        return super().formfield_for_foreignkey(db_field, request, **kwargs) 
    
    actions = ["mark_submitted", "mark_approved", "mark_rejected"]
    @admin.action(description="durumu: Gönderildi (submitted) yap") 
    def mark_submitted(self, request, queryset):
        for obj in queryset: obj.to_submitted()
    @admin.action(description="Durumu: Onaylandı (approved) yap")
    def mark_approved(self, request, queryset):
        for obj in queryset: obj.to_approved()
    @admin.action(description="Durumu: Reddedildi (rejected) yap")
    def mark_rejected(self, request, queryset):
        for obj in queryset: obj.to_rejected()
        
@admin.register(Finding)
class FindingAdmin(admin.ModelAdmin):
    list_display = ("audit", "severity")
    inlines = [ActionInline]

admin.site.register([Action, Todo])
        
        
        