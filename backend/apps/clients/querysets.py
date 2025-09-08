from django.db import models

class ClientQuerySet(models.QuerySet):
    def for_user(self, user):
        if not user.is_authenticated:
            return self.none()
        ac = getattr(user, "active_company_id", None)
        if ac:
            return self.filter(company_id=ac)
        try:
            return self.filter(company__in=user.companies.all()).distinct()
        except Exception:
            return self.none()