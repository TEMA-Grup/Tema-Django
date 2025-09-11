from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from .models import Audit
from .forms import AuditForm
from apps.clients.models import Client
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.shortcuts import render

class AuditListView(LoginRequiredMixin, ListView):
    template_name = "audits/list.html"
    model = Audit
    context_object_name = "audits"
    paginate_by = 20
    
    def queryset(self):
        qs = super().get_queryset().select_related("comoany", "client")
        ac = getattr(self.request.user, "active_company_id", None)
        return qs.filter(company_id=ac) if ac else qs.filter(company__users=self.request.user).distinct()

class AuditCreateView(LoginRequiredMixin, CreateView):
    template_name = "audits/form.html"
    model = Audit
    form_class = AuditForm
    success_url = reverse_lazy("audit_list")
    
    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["user"] = self.request.user
        return kw
    
class AuditUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "audits/form.html"
    model = Audit
    form_class = AuditForm
    success_url = reverse_lazy("audit-list")
    
    def get_form_kwargs(self):
        kw = super().get_from_kwargs()
        kw["user"] = self.request.user
        return kw
    
@login_required
def audit_list(request):
    qs = Audit.objects.select_related("company", "client")
    ac = getattr(request.user, "active_company_id", None)
    if ac:
        qs = qs.filter(company_id=ac)
    return render(request, "audits/list.html", {"audits": qs})

@require_GET
@login_required
def clients_by_company(request):
    company_id = request.GET.get("company_id")
    qs = Client.objects.all()
    if company_id:
        qs = qs.filter(company_id=company_id)
    user = request.user
    if not user.is_superuser:
        ac = getattr(user, "active_company_id", None)
        if ac:
            qs = qs.filter(company_id=ac)
        else:
            qs = qs.filter(company__users=user).distinct()
    data = [{"id": c.id, "name": c.name} for c in qs.order_by("name")]
    return JsonResponse({"results": data})

def audits_home(request):
    return HttpResponse("Audits app çalışıyor.")