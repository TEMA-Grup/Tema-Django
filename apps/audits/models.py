from django.db import models
from django.conf import settings
from django.db import transaction
from django.db.models import F
from django.core.exceptions import ValidationError
from .querysets import AuditQuerySet

class Sequence(models.Model):
    code = models.CharField(max_length=64)
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE, related_name="sequences")
    prefix = models.CharField(max_length=32, default="AUD-")
    padding = models.PositiveSmallIntegerField(default=5)
    last_number = models.IntegerField(default=0)
    
    class Meta:
        unique_together = (("code", "company"),)
        
    def __str__(self):
        return f"{self.company}::{self.code}"
    
    @transaction.atomic
    def next_value(self) -> str:
        type(self).objects.select_for_update().get(pk=self.pk)
        self.last_number = F("last_number") + 1
        self.save(update_fields=["last_number"])
        self.refresh_from_db()
        return f"{self.prefix}{str(self.last_number).zfill(self.padding)}"
    
def next_code(code: str, company_id: int) -> str:
    seq, _ = Sequence.objects.get_or_create(
        code=code,
        company_id=company_id,
        defaults={"prefix": "AUD-", "padding": 5, "last_number": 0},
    )
    return seq.next_value()

class Audit(models.Model):
    TYPE_CHOICES = [
        ("internal", "İç Denetim"),
        ("external", "Dış Denetim"),
        ("compliance", "Uyum Denetimi"),
        ("risk", "Risk Tabanlı"),
    ]
    STATE_CHOICES = [
        ("draft", "Taslak"),
        ("submitted", "Gönderildi"),
        ("approved", "Onaylandı"),
        ("rejected", "Reddedildi"),
    ]
    
    company = models.ForeignKey("companies.Company", on_delete=models.PROTECT, related_name="audits")
    client = models.ForeignKey("clients.Client", on_delete=models.PROTECT, related_name="audits")
    name = models.CharField("Denetim Adı", max_length=200)
    reference = models.CharField("Referans", max_length=64, unique=True, blank=True)
    audit_type = models.CharField("Tür", max_length=20, choices=TYPE_CHOICES, default="internal")
    auditor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    audit_date = models.DateField("Tarih", null=True, blank=True)
    objects = AuditQuerySet.as_manager()
    state = models.CharField(max_length=16, choices=STATE_CHOICES, default="draft")
    progress = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["company", "reference"], name="uniq_audit_company_reference")
        ]
    
    def __str__(self):
        return f"{self.reference or '_'} {self.name}"
    
    def compute_progress(self):
        mapping = {"draft": 10, "submitted": 40, "approved": 100, "rejected": 0}
        self.progress = mapping.get(self.state, 0)
        
    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.reference and self.company_id:
            self.reference = next_code("audits.audit", self.company_id)
        self.compute_progress()
        super().save(*args, **kwargs)
    
    def to_submitted(self):
        self.state = "submitted"; self.compute_progress(); self.save(update_fields=["state", "progress"])
        
    def to_approved(self):
        self.state = "approved"; self.compute_progress(); self.save(update_fields=["state", "progress"])
     
    def to_rejected(self):
        self.state = "rejected"; self.compute_progress(); self.save(update_fields=["state", "progress"])    
    
    def clean(self):
        super().clean()
        if self.client_id and self.company_id and self.client.company_id != self.company_id:
            raise ValidationError("Client, seçili company ile aynı şirkete bağlı olmalı.")
        
class Finding(models.Model):
    SEVERITY = [("low", "Düşük"), ("medium", "Orta"), ("high", "Yüksek")]
    audit = models.ForeignKey(Audit, on_delete=models.CASCADE, related_name="findings")
    description = models.TextField("Bulgunun Açıklaması")
    severity = models.CharField(max_length=10, choices=SEVERITY, default="medium")
    def __str__(self): return f"{self.audit.reference} - {self.severity}"
    
class Action(models.Model):
    findings = models.ForeignKey(Finding, on_delete=models.CASCADE, related_name="actions")
    action_description = models.TextField("Aksiyon")
    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    deadline = models.DateField(null=True, blank=True)
    state = models.CharField(max_length=20, choices=[("open", "Açık"), ("progress", "Devam"), ("done", "Tamam")], default="open")
    def __str__(self): return  f"Aksiyon for {self.finding_id}"

class Todo(models.Model):
    audit = models.ForeignKey(Audit, on_delete=models.CASCADE, related_name="todos")
    task = models.CharField(max_length=200)
    done = models.BooleanField(default=False)
    deadline = models.DateField(null=True, blank=True)
    def __str__(self): return self.task
    
class Attachment(models.Model):
    audit = models.ForeignKey(Audit, on_delete=models.CASCADE,related_name="attachments")
    file = models.FileField(upload_to="audit_attachments/%Y/%m/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.audit.reference} - {self.file.name}"