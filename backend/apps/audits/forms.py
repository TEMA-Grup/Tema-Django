from django import forms
from .models import Audit

class AuditForm(forms.ModelForm):
    class Meta:
        model = Audit
        fields = ["company", "client", "name", "audit_type", "auditor", "audit_date"]
        def __init__(self, *args, **kwargs):
            user = kwargs.pop("user", None)
            super().__init__(*args, **kwargs)
            if user and not user.is_superuser:
                ac = getattr(user, "active_company_id", None)
                if ac:
                    self.fields["company"].queryset = self.fields["company"].queryset.filter(id=ac)
                    self.fields["client"].queryset = self.fields["client"].queryset.filter(company_id=ac)
                else:
                    self.fields["company"].queryset = self.fields["company"].queryset.filter(users=user).distinct()
                    self.fields["client"].queryset = self.fields["client"].queryset.filter(company__users=user).distinct()