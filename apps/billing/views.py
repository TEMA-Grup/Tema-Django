from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.core.decorators import require_plugin
from .models import Invoice
from .forms import InvoiceForm

@login_required
@require_plugin("billing")
def invoice_list(request):
    qs = Invoice.objects.all()
    if getattr(request, "tenant", None):
        qs = qs.filter(company=request.tenant)
    return render(request, "billing/invoice_list.html", {"invoices": qs})

@login_required
@require_plugin("billing")
def invoice_create(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            inv = form.save(commit=False)
            inv.created_by = request.user
            inv.company = request.tenant
            inv.save()
            return redirect("billing:list")
    else:
        form = InvoiceForm()
    return render(request, "billing/invoice_form.html", {"form": form})

@login_required
@require_plugin("billing")
def invoice_edit(request, pk):
    inv = get_object_or_404(Invoice, pk=pk)
    if getattr(request, "tenant", None):
        if inv.tenant_id != request.tenant.id:
            return redirect("billing:list")
    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=inv)
        if form.is_valid():
            form.save()
            return redirect("billing:list")
    else:
        form = InvoiceForm(instance=inv)
    return render(request, "billing/invoice_form.html", {"form": form})