from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from apps.companies.models import Company

@require_POST
@login_required
def switch_company(request):
    cid = request.POST.get("company_id")
    company = get_object_or_404(Company, id=cid, users=request.user)
    request.session["active_company_id"] = company.id
    request.user.active_company = company
    request.user.save(update_fields=["active_company"])
    return redirect(request.META.get("HTTP_REFERER") or "admin:index")

def accounts_home(request):
    return HttpResponse("Accounts sayfası çalışıyor")