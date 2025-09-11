from django.db import models
from django.core.exceptions import ValidationError

SECTORS = [
    ("it", "Bilişim/IT"),
    ("manufacturing", "İmalat"),
    ("finance", "Finans"),
    ("retail", "Perakende"),
    ("health", "Sağlık"),
    ("energy", "Enerji"),
    ("construction", "İnşaat"),
    ("education", "Eğitim"),
    ("public", "Kamu"),
    ("other", "Diğer")
]

class Sector(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.name

class Company(models.Model):
    name = models.CharField("Kısa Ad", max_length=120, unique=True, help_text="Listelerde görünecek kısa ad")
    legal_title = models.CharField("Unvan", max_length=255, blank=True)
    vat_number = models.CharField("Vergi No", max_length=64, blank=True)
    staff_count = models.PositiveIntegerField("Personel Sayısı", null=True, blank=True)
    founded_year = models.PositiveSmallIntegerField("Kuruluş Yılı", null=True, blank=True)
    sector = models.ForeignKey("companies.Sector", null=True, blank=True, on_delete=models.SET_NULL, related_name="companies")
    
    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["vat_number"]),
        ]
    def __str__(self):
        return self.name or self.legal_title
    
    def clean(self):
        super().clean()
        if self.founded_year:
            import datetime
            if self.founded_year < 1800 or self.founded_year > datetime.date.today().year:
                raise ValidationError({"founded year": "Kuruluş yılı 1800 ile bugünün yılı arasında olmalı."})