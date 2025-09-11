from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class User(AbstractUser):
    companies = models.ManyToManyField("companies.Company", blank=True, related_name="users")
    active_company = models.ForeignKey(
        "companies.Company", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+"
    )
    
    def clean(self):
        super().clean()
        if self.active_company and self.pk:
            if not self.companies.filter(pk=self.active_company_id).exists:
              raise ValidationError("Active company, user's company arasında olmalı.")
     
    def set_active_company(self, company): 
        if not self.companies.filter(pk=company.pk).exists():
            raise ValidationError("Bu kullanıcı bu şirkete bağlı değil.")
        self.active_company = company
        self.save(update_fields=["active_company"])      

