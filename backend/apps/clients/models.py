from django.db import models
from .querysets import ClientQuerySet

class Client(models.Model):
    company = models.ForeignKey("companies.Company", on_delete=models.PROTECT, related_name="clients")
    name = models.CharField("Müşteri Adı", max_length=200)
    email = models.EmailField("E-posta", blank=True)
    phone = models.CharField("Telefon", max_length=50, blank=True)
    notes = models.TextField("Notlar", blank=True)
    objects = ClientQuerySet.as_manager()
    class Meta:
        ordering = ["name"]
        unique_together = (("company", "name"),)
        
    def __str__(self):
        return f"{self.name} ({self.company})"