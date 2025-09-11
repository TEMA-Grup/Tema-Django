from django.db import models

class AuditQuerySet(models.QuerySet):
    def for_user(self, user):
        if not user.is_authenticated:
            return self.none()
        
        ac = getattr(user, "active_company_id", None)
        if ac:
            return self.filter(company_id=ac)
        
        return self.filter(company_in=user.companies.all()).distinct()