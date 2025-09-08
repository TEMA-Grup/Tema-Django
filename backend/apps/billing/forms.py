from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ["number", "customer_name", "amount", "issue_date", "due_date", "status"]