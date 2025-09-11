from django.db import models

class Plugin(models.Model):
    code = models.SlugField(max_length=64, unique=True)
    title = models.CharField(max_length=120)
    version = models.CharField(max_length=32, default="0.1.0")
    is_core = models.BooleanField(default=False)
    enabled_globally = models.BooleanField(default=False)
    
    class Meta:
        ordering = ["code"]
        
    def __str__(self):
        return f"{self.code} ({self.version})"
    
class CompanyPlugin(models.Model):
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE, related_name="company_plugins")
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE, related_name="company_links")
    enabled = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ("company", "plugin")
        
    def __str__(self):
        return f"{self.company} -> {self.plugin.code} ({'ON' if self.enabled else 'OFF'})"
