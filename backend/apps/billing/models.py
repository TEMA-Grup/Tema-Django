from django.db import models
from django.conf import settings

class Invoice(models.Model):
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE, related_name="invoices")
    number = models.CharField(max_length=64, unique=True)
    customer_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    issue_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    
    class Status(models.TextChoices):
        DRAFT = "draft", "Taslak"
        SENT = "sent", "Gönderildi"
        PAID = "paid", "Ödendi"
        CANCELED = "canceled", "İptal"
        
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DRAFT)
    
    def __str__(self):
        return f"{self.number} - {self.customer_name}"